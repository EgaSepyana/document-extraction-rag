from pydantic import Field, BaseModel
from typing import List, Optional
from api.model import FindDTO
from sqlalchemy.ext.declarative import declarative_base
from api.config.base import settings
from sqlalchemy import Column, Integer, String, Boolean, Float, ARRAY, DateTime, JSON

Base = declarative_base()

class DocumentDTO(BaseModel):
    id: Optional[str] = Field(None)
    
    file_name: Optional[str] = Field(default=None)
    file_size: Optional[str] = Field(default=None)
    file_path : Optional[str] = Field(default=None)
    file_extention : Optional[str] = Field(default=None)
    category : Optional[str] = Field(default=None)
    description : Optional[str] = Field(default=None)
    indexing : Optional[bool] = Field(default=None)
    contents : Optional[str] = Field(default=None) 

class UpdateDocumentDTO(DocumentDTO):
    id: str


# class Document(Base):
#     __tablename__ = settings.POSTGRESQL_TABLE_DOCUMENT
#     id = Column(String, primary_key=True, index=True)
#     created_at = Column(DateTime , nullable=True)
#     name = Column(String, index=True)