import os
from time import time
from fastapi import File, UploadFile, HTTPException, Depends, APIRouter, Body
from api.util.helper import get_execution_time, router_param_builder, is_include_schema
from api.model.base_response import BaseResponseFailed, BaseResponse
from api.model.metadata import MetadataSuccess, MetadataFailed
from api.model.pagination import Pagination
from api.model import FindDTO
from api.model.qna import QnaDTO, IndexingRequestDTO, ChatRequestDTO
from api.model.document import DocumentDTO
from api.service.qna import QnaService
import traceback

obj = QnaService()
tag = os.path.splitext(os.path.basename(os.path.abspath(__file__)))[0]
router = APIRouter(**router_param_builder(tag))


@router.post("/upload", include_in_schema=is_include_schema(tag, "add"))
async def upload(file: UploadFile = File(...), dto: DocumentDTO = Depends()):
    start_time = time()
    try:
        return BaseResponse(
            data=obj.upload(file, dto),
            metaData=MetadataSuccess(execution_time=get_execution_time(start_time)),
        )
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(
            status_code=400,
            detail=BaseResponseFailed(
                metaData=MetadataFailed(
                    execution_time=get_execution_time(start_time), message=str(error)
                )
            ).dict(),
        )


@router.post("/index", include_in_schema=is_include_schema(tag, "add"))
async def index(dto: IndexingRequestDTO):
    start_time = time()
    try:
        return BaseResponse(
            data=obj.index(dto),
            metaData=MetadataSuccess(execution_time=get_execution_time(start_time)),
        )
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(
            status_code=400,
            detail=BaseResponseFailed(
                metaData=MetadataFailed(
                    execution_time=get_execution_time(start_time), message=str(error)
                )
            ).dict(),
        )


@router.post("/chat", include_in_schema=is_include_schema(tag, "add"))
async def chat(dto: ChatRequestDTO):
    start_time = time()
    try:
        return BaseResponse(
            data=obj.chat(dto),
            metaData=MetadataSuccess(execution_time=get_execution_time(start_time)),
        )
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(
            status_code=400,
            detail=BaseResponseFailed(
                metaData=MetadataFailed(
                    execution_time=get_execution_time(start_time), message=str(error)
                )
            ).dict(),
        )


@router.post("/docs/get-all", include_in_schema=is_include_schema(tag, "add"))
async def get_all(dto: FindDTO):
    start_time = time()
    try:
        data, count = obj.get_all(dto)
        return BaseResponse(
            data=data,
            metaData=MetadataSuccess(
                pagination=Pagination.count_total_pages(dto.size, count),
                execution_time=get_execution_time(start_time),
            ),
        )
    except Exception as error:
        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=400,
            detail=BaseResponseFailed(
                metaData=MetadataFailed(
                    execution_time=get_execution_time(start_time), message=str(error)
                )
            ).dict(),
        )


@router.get("/docs/{id}", include_in_schema=is_include_schema(tag, "add"))
async def chat(id: str):
    start_time = time()
    try:
        return BaseResponse(
            data=obj.docs(id),
            metaData=MetadataSuccess(execution_time=get_execution_time(start_time)),
        )
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(
            status_code=400,
            detail=BaseResponseFailed(
                metaData=MetadataFailed(
                    execution_time=get_execution_time(start_time), message=str(error)
                )
            ).dict(),
        )


@router.get(
    "/docs/conversation/{chatId}", include_in_schema=is_include_schema(tag, "add")
)
async def chat(chatId: str):
    start_time = time()
    try:
        data, _ = obj.get_conversation(chatId)
        return BaseResponse(
            data=data,
            metaData=MetadataSuccess(execution_time=get_execution_time(start_time)),
        )
    except Exception as error:
        traceback.print_exc()
        raise HTTPException(
            status_code=400,
            detail=BaseResponseFailed(
                metaData=MetadataFailed(
                    execution_time=get_execution_time(start_time), message=str(error)
                )
            ).dict(),
        )


# @router.put("/update", include_in_schema=is_include_schema(tag, "update"))
# async def update(dto: UpdateQnaDTO):
#     start_time = time()
#     try:
#         return BaseResponse(data=obj.update(dto),
#                             metaData=MetadataSuccess(execution_time=get_execution_time(start_time)))
#     except Exception as error:
#         raise HTTPException(status_code=400, detail=BaseResponseFailed(
#             metaData=MetadataFailed(execution_time=get_execution_time(start_time),
#                                     message=str(error))).dict())


# @router.delete("/delete", include_in_schema=is_include_schema(tag, "delete"))
# async def delete(id):
#     start_time = time()
#     try:
#         return BaseResponse(data=obj.delete(id),
#                             metaData=MetadataSuccess(execution_time=get_execution_time(start_time)))
#     except Exception as error:
#         raise HTTPException(status_code=400, detail=BaseResponseFailed(
#             metaData=MetadataFailed(execution_time=get_execution_time(start_time),
#                                     message=str(error))).dict())


# @router.post("/get-all", include_in_schema=is_include_schema(tag, "get-all"))
# async def get_all(dto: FindDTO):
#     start_time = time()
#     try:
#         data, count = obj.get_all(dto)
#         return BaseResponse(data=data,
#                             metaData=MetadataSuccess(pagination=Pagination.count_total_pages(dto.size, count),
#                                                      execution_time=get_execution_time(start_time)))
#     except Exception as error:
#         raise HTTPException(status_code=400, detail=BaseResponseFailed(
#             metaData=MetadataFailed(execution_time=get_execution_time(start_time),
#                                     message=str(error))).dict())


# @router.get("/get-one", include_in_schema=is_include_schema(tag, "get-one"))
# async def get_by_id(id: str):
#     start_time = time()
#     try:
#         data = obj.get_by_id(id)
#         if data is None:
#             raise Exception(f"There is no data with id: {id}")
#         return BaseResponse(data=data,
#                             metaData=MetadataSuccess(execution_time=get_execution_time(start_time)))
#     except Exception as error:
#         raise HTTPException(status_code=400, detail=BaseResponseFailed(
#             metaData=MetadataFailed(execution_time=get_execution_time(start_time),
#                                     message=str(error))).dict())
