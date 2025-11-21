from chromadb import HttpClient
import chromadb
from chromadb.config import Settings
import json
from service.extractor import Extraktor
from service.embedder import Embedler
from loguru import logger
from uuid import uuid4


class VectorStores:
    def __init__(self):
        self.embedler = Embedler()
        self.extractor = Extraktor()
        self.collection_name = "ega-document"
        self.persistence_name = "./chroma_data"
        self.CHROMA_SETTINGS = Settings(
            anonymized_telemetry=False,
        )

    def test_query(self, query):
        # vectro_strore = VectorStores()

        embedler = Embedler()
        query_embeding = embedler.embed_documents(query)

        results = self.search_similar(query_embeding)
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        print(docs)
        print(metas)

    def main(self):

        file_path = "public/bitcoin.pdf"

        texts = self.extractor.extract_file(file_path)
        chunks = self.extractor.indexing_text(texts)
        embedings = self.embedler.embed_documents(chunks)
        doc_id = str(uuid4()).replace("-", "")

        metadata = {
            "file_path": file_path,
            "id": doc_id,
        }

        # print(chunks)
        # print(embedings)

        self.add_embeddings(doc_id, embedings, chunks, metadata)
        # self.add_embeding_seq(doc_id, embedings, chunks, metadata)

        # collection.add(
        #     documents=["This is document1", "This is document2"], # we handle tokenization, embedding, and indexing automatically. You can skip that and add your own embeddings as well
        #     metadatas=[{"source": "notion"}, {"source": "google-docs"}], # filter on these!
        #     ids=["doc1", "doc2"], # unique for each doc
        # )

        # print(json.dumps(results , indent=4))

    def add_embeddings(self, doc_id, embeddings, chunks, metadata):
        logger.info("====Staring Embed Document=====")
        # client = HttpClient(host="localhost", port=8000)
        client = chromadb.PersistentClient(
            self.persistence_name, settings=self.CHROMA_SETTINGS
        )
        collection = client.get_or_create_collection(
            self.collection_name, metadata={"hnsw:space": "cosine"}
        )

        metadatas = []

        for i in chunks:
            copy = metadata.copy()
            copy["total_chunks"] = len(chunks)
            copy["chunk"] = i
            metadatas.append(copy)

        collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=[f"{doc_id}-{i}" for i in range(len(chunks))],
        )

    def add_embeding_seq(self, doc_id, embeddings, chunks, metadata):
        logger.info("====Staring Embed Document=====")
        # client = HttpClient(host="localhost", port=8000)
        client = chromadb.PersistentClient(
            self.persistence_name, settings=self.CHROMA_SETTINGS
        )
        collection = client.get_or_create_collection(
            self.collection_name, metadata={"hnsw:space": "cosine"}
        )

        for i, chunk in enumerate(chunks):
            embeding = self.embedler.embed(chunk)

            collection.add(
                documents=[chunk],
                embeddings=[embeding],
                metadatas=[metadata],
                ids=[f"{doc_id}-{i}"],
            )

    def search_similar(self, query_embedding, top_k=3, query=None) -> list:
        # client = HttpClient(host="localhost", port=8000)
        client = chromadb.PersistentClient(
            self.persistence_name, settings=self.CHROMA_SETTINGS
        )
        collection = client.get_collection(self.collection_name)

        results = collection.query(
            query_embeddings=query_embedding, n_results=top_k, where=query
        )

        return results

    def search(self, text: str):
        client = chromadb.PersistentClient(
            self.persistence_name, settings=self.CHROMA_SETTINGS
        )
        collection = client.get_collection(self.collection_name)

        results = collection.query(
            query_texts=[text],
            n_results=100,
        )

        docs = results["documents"][0]
        metas = results["metadatas"][0]
        print(docs)
        print(metas)

        return docs
        # return results


if __name__ == "__main__":
    vectro_strore = VectorStores()

    embedler = Embedler()
    query_embeding = embedler.embed_documents("how bitcoint works?")

    results = vectro_strore.search_similar(query_embeding)
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    print(docs)
    print(metas)
