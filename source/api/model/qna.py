from pydantic import Field, BaseModel
from typing import List, Optional
from api.model import FindDTO
from sqlalchemy.ext.declarative import declarative_base
from api.config.base import settings
from sqlalchemy import Column, Integer, String, Boolean, Float, ARRAY, DateTime, JSON

Base = declarative_base()

class QnaDTO(BaseModel):
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(default=None)

class ChatRequestDTO(BaseModel):
    question : str
    document_id : str = Field(default=None)

class IndexingRequestDTO(BaseModel):
    document_id : str
    chunk_size : Optional[int] = Field(default=1000)
    overlap_size : Optional[int] = Field(default=150)

class UploadDTO(BaseModel):
    pass

class QnaIndexDTO(BaseModel):
    document_id: Optional[str] = Field(default=None)
    # chunk_size: Optional[int] = Field(default=500)
    # overlap_size: Optional[int] = Field(default=50)  
    