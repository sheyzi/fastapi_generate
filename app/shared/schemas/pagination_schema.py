from typing import TypeVar, Generic

from pydantic import BaseModel

T = TypeVar("T")


# Create a generic pagination response schema
class PaginationResponse(BaseModel, Generic[T]):
    total: int
    page: int
    limit: int
    pages: int
    data: list[T]
