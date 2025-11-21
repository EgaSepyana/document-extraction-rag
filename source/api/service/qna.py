# -*- coding: utf-8 -*-
import json
from api.config.base import settings
from loguru import logger
from datetime import datetime
from api.util.postgresql import (
    PostgresqlService,
    get_db,
    auto_insert_table,
    auto_update_table,
    get_one,
)
from api.model import FindDTO
from api.model.qna import QnaDTO, IndexingRequestDTO, ChatRequestDTO
from sqlalchemy.exc import IntegrityError
from fastapi import UploadFile
from api.util.helper import get_md5, orm_to_dict, row_to_dict
from uuid import uuid4
from db.vector_store import VectorStores
from service.extractor import Extraktor
from service.embedder import Embedler
from service.llm_client import LLM
import shutil
from api.model.document import UpdateDocumentDTO


class QnaService:
    def __init__(self):
        pass
        self.pg_engine = PostgresqlService(url=settings.BASE_POSTGRESQL_URL)
        self.db_pg = next(get_db(self.pg_engine))
        self.vector_stores = VectorStores()
        self.extractor = Extraktor()
        self.embedler = Embedler()
        self.llm_client = LLM()

    def upload(self, file: UploadFile, dto: UpdateDocumentDTO):
        file_id: str = str(uuid4()).replace("-", "")
        file_name = file.filename
        file_extention = file.filename.split(".")[-1]
        file_size = file.size
        file_path = f"public/{file_id}.{file_extention}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        dto.id = file_id
        dto.file_name = file_name
        dto.file_size = file_size
        dto.file_path = file_path
        dto.file_extention = file_extention
        dto.indexing = False
        dto.contents = "".join(
            [text["text"] for text in self.extractor.extract_file(file_path)]
        )

        document = dto.model_dump()
        document["created_at"] = datetime.now()
        document["updated_at"] = datetime.now()

        # print(isinstance(document["indexing"] , bool))

        auto_insert_table("document", "ega", [document], self.pg_engine)

        return document

    def index(self, dto: IndexingRequestDTO):
        document_id = dto.document_id
        chunk_size = dto.chunk_size
        overlap_size = dto.overlap_size

        document = get_one("document", "ega", self.db_pg, "id", document_id)
        if not document:
            raise Exception("Document Is Not Exist")

        if document.get("indexing") == False:
            chunks = self.extractor.indexing_text(
                document["contents"], chunk_size, overlap_size
            )
            logger.info(chunks)
            embeddings = self.embedler.embed_documents(chunks)

            metadata = document.copy()
            metadata.pop("contents")
            metadata.pop("indexing")
            metadata.pop("created_at")
            metadata.pop("updated_at")
            self.vector_stores.add_embeddings(document_id, embeddings, chunks, metadata)
            auto_update_table(
                "document",
                "ega",
                [{"id": document_id, "indexing": True}],
                self.pg_engine,
                "id",
            )

        return {
            "document_id": document_id,
            "messege": "document is successfuly indexed",
            "indexing": True,
        }

    def chat(self, dto: ChatRequestDTO):
        query = dto.question
        document_id = dto.document_id

        answer = None

        if document_id:
            query_metadata = {
                "$or": [
                    {"id": document_id},
                    {"id": document_id},
                ]
            }
            answer = self.llm_client.generate_answer(
                query, top_k=3, query_metadata=query_metadata, chatId=document_id
            )
        else:
            answer = self.llm_client.generate(query)

        self.addConversation(document_id, query, answer.get("answer"))

        return answer

    def get_all(self, dto: FindDTO):
        from sqlalchemy import cast, String, Table, MetaData, and_, or_
        from sqlalchemy.orm import aliased

        db_pg = next(get_db(self.pg_engine))

        Document = Table("document", MetaData(schema="ega"), autoload_with=db_pg.bind)

        query = db_pg.query(
            Document.c.id,
            Document.c.file_name.label("fileName"),
            Document.c.created_at.label("createdAt"),
        ).filter(Document.c.indexing == True)

        query = query.order_by(Document.c.created_at.desc())

        def retrieve_data(dto, query):
            total_count = query.count()
            data = query.offset((dto.page - 1) * dto.size).limit(dto.size).all()
            return data, total_count

        try:
            data, total_count = retrieve_data(dto, query)
        except Exception as e:
            if "please rollback() fully before proceeding" in str(e).lower():
                db_pg.rollback()
                data, total_count = retrieve_data(dto, query)
            else:
                raise e
        finally:
            db_pg.close()

        if isinstance(data, list):
            return [row_to_dict(datum) for datum in data], total_count
        else:
            return [], 0

    def get_conversation(self, documentId: str):
        from sqlalchemy import cast, String, Table, MetaData, and_, or_
        from sqlalchemy.orm import aliased

        db_pg = next(get_db(self.pg_engine))

        Conversation = Table(
            "conversation", MetaData(schema="ega"), autoload_with=db_pg.bind
        )

        query = db_pg.query(
            Conversation.c.id,
            Conversation.c.contents.label("messege"),
            Conversation.c.isUser.label("isUser"),
            Conversation.c.created_at.label("timestamp"),
        ).filter(Conversation.c.chat_id == documentId)

        query = query.order_by(Conversation.c.created_at.asc())

        def retrieve_data(query):
            total_count = query.count()
            data = query.all()
            return data, total_count

        try:
            data, total_count = retrieve_data(query)
        except Exception as e:
            if "please rollback() fully before proceeding" in str(e).lower():
                db_pg.rollback()
                data, total_count = retrieve_data(query)
            else:
                raise e
        finally:
            db_pg.close()

        if isinstance(data, list):
            return [row_to_dict(datum) for datum in data], total_count
        else:
            return [], 0

    def docs(self, document_id: str):
        document = get_one("document", "ega", self.db_pg, "id", document_id)
        if not document:
            raise Exception("Document Is Not Exist")

        return document

    def addConversation(self, chatId: str, query: str, answer: str):

        messege_user = {
            "id": str(uuid4()).replace("-", ""),
            "chat_id": chatId,
            "isUser": True,
            "contents": query,
            "created_at": datetime.now(),
        }

        messege_ai = {
            "id": str(uuid4()).replace("-", ""),
            "chat_id": chatId,
            "isUser": False,
            "contents": answer,
            "created_at": datetime.now(),
        }

        auto_insert_table(
            "conversation", "ega", [messege_user, messege_ai], self.pg_engine
        )
        return True

    # def update(self, dto: UpdateQnaDTO):
    #     dict_dto = {key: value for key, value in dto.dict().items()}
    #     data = Qna(**dict_dto)
    #     try:
    #         merged_obj = self.db_pg.merge(data)
    #         self.db_pg.commit()
    #         self.db_pg.refresh(merged_obj)
    #     except Exception:
    #         self.db_pg.rollback()
    #         raise
    #     return dict_dto

    # def get_by_id(self, _id):
    #     data = self.db_pg.query(Qna).filter(Qna.id == _id).first()
    #     if not data:
    #         return None
    #     return orm_to_dict(data)

    # def get_all(self, dto: FindDTO):
    #     from sqlalchemy import and_, or_
    #     query = self.db_pg.query(Qna)
    #     filters = []

    #     if dto.search and dto.search_by:
    #         search_conditions = []
    #         for field in dto.search_by:
    #             column = getattr(Qna, field, None)
    #             if column is not None:
    #                 if dto.operator == "and":
    #                     search_words = dto.search.split()
    #                     word_conditions = [column.ilike(f"%{word}%") for word in search_words]
    #                     search_conditions.append(and_(*word_conditions))
    #                 else:
    #                     search_conditions.append(column.ilike(f"%{dto.search}%"))
    #         if search_conditions:
    #             filters.append(or_(*search_conditions))
    #     elif dto.search:
    #         filters.append(Qna.name.ilike(f"%{dto.search}%"))

    #     if dto.filters:
    #         for filter_item in dto.filters:
    #             field = filter_item.get("field")
    #             operator = filter_item.get("operator")
    #             value = filter_item.get("value", {})
    #             if not field or not operator:
    #                 continue
    #             column = getattr(Qna, field, None)
    #             if column is None:
    #                 continue

    #             if operator == "is" and value.get("is") is not None:
    #                 filters.append(column == value["is"])
    #             elif operator == "is not" and value.get("is") is not None:
    #                 filters.append(column != value["is"])
    #             elif operator == "is one of" and value.get("isOneOf"):
    #                 filters.append(column.in_(value["isOneOf"]))
    #             elif operator == "is not one of" and value.get("isOneOf"):
    #                 filters.append(~column.in_(value["isOneOf"]))
    #             elif operator == "greater than equals" and value.get("gte") is not None:
    #                 filters.append(column >= value["gte"])
    #             elif operator == "less than equals" and value.get("lte") is not None:
    #                 filters.append(column <= value["lte"])
    #             elif operator == "is between" and value.get("gte") is not None and value.get("lte") is not None:
    #                 filters.append(column.between(value["gte"], value["lte"]))
    #             elif operator == "is not between" and value.get("gte") is not None and value.get("lte") is not None:
    #                 filters.append(~column.between(value["gte"], value["lte"]))
    #             elif operator == "is exist":
    #                 filters.append(column.isnot(None))
    #             elif operator == "is not exist":
    #                 filters.append(column.is_(None))
    #             elif operator == "is contains" and value.get("is"):
    #                 filters.append(column.ilike(f"%{value['is']}%"))

    #     if filters:
    #         query = query.filter(and_(*filters))

    #     def retrieve_data(dto, query):
    #         total_count = query.count()
    #         data = query.offset((dto.page - 1) * dto.size).limit(dto.size).all()
    #         return data, total_count

    #     try:
    #         data, total_count = retrieve_data(dto, query)
    #     except Exception as e:
    #         if "please rollback() fully before proceeding" in str(e).lower():
    #             self.db_pg.rollback()
    #             data, total_count = retrieve_data(dto, query)
    #         else:
    #             raise e

    #     if isinstance(data, list):
    #         return [orm_to_dict(datum) for datum in data], total_count
    #     else:
    #         return [], 0

    def add(self, dto: QnaDTO):
        _id = dto.id
        if not _id:
            _id = get_md5(
                get_md5(f"{json.dumps(dto.model_dump())}_{datetime.now().timestamp()}")
            )
        data = self.get_by_id(_id)
        if not data:
            data = dto.dict()
            data["created_at"] = datetime.now()
            data["id"] = _id
            return self.insert(data)
        else:
            logger.info(f"Data already exist")
            raise Exception(f"data already exist!")

    # def insert(self, dto):
    #    data = Qna(**dto)
    #    try:
    #        self.db_pg.add(data)
    #        self.db_pg.commit()
    #        self.db_pg.refresh(data)
    #    except IntegrityError as err:
    #        self.db_pg.rollback()
    #        if err.orig.pgcode == "23505":
    #            return f"Duplicate ID: {data.id}"
    #        else:
    #            raise
    #    except Exception:
    #        self.db_pg.rollback()
    #        raise

    #    return dto

    # def delete(self, _id):
    #     data = self.db_pg.query(Qna).filter(Qna.id == _id).first()
    #     if not data:
    #         raise Exception(f"There is no data with id: {_id}")
    #     self.db_pg.delete(data)
    #     self.db_pg.commit()
    #     return {"message": f"Data id {_id} has been deleted"}
