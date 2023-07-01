from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, PaginationParameters
from app.shared.schemas.pagination_schema import PaginationResponse
from .schemas import UserCreate, UserRead
from .repositories import user_repo

user_router = APIRouter()


@user_router.get("/", response_model=PaginationResponse[UserRead])
def get_users(
    pagination: Annotated[PaginationParameters, Depends(PaginationParameters)],
    db: Annotated[Session, Depends(get_db)],
):
    return user_repo.get_multi(db, pagination)


@user_router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    former_user = user_repo.get_by_email(db, data.email)

    if former_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User details already exist",
        )
    return user_repo.create(db, obj_in=data)
