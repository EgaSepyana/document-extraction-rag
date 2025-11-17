from typing import Any
from pydantic import BaseModel, Field


class CustomBaseModel(BaseModel):
    def dict(self, *, include: Any = None, exclude: Any = None, by_alias: bool = False, exclude_unset: bool = True, **kwargs) -> dict:
        return super().dict(include=include, exclude=exclude, by_alias=by_alias, exclude_unset=exclude_unset, **kwargs)


class BaseFindDTO(BaseModel):
    search: str = Field(default=None)
    search_by: list = Field(default=[])
    operator: str = Field(default=None)
    orderBy: str = Field(default="createdAt")
    order: str = Field(default="desc")
    page: int = Field(default=1)
    size: int = Field(default=10)
    searchIgnoreSpecial: bool = Field(default=False)


class FindDTO(BaseFindDTO):
    workspaceId: str = Field(default=None)
    filters: list = Field(default=[])
    organizationId: str = Field(default=None)

class ConnectionFindDTO(FindDTO):
    readWrite: bool = Field(default=False)
