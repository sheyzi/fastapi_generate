from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from core.dependency import get_db, get_active_user
from schemas.users import UserCreate, UserOut
from schemas.auth import EmailSchema, RefreshDetails, Token, LoginDetails

from . import views

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/register/", response_model=UserOut, status_code=201)
def register_user(user_details: UserCreate, db: Session = Depends(get_db)):
    user = views.create_user(user_details, db)
    return user


@auth_router.post("/login/", response_model=Token)
def login(user_details: LoginDetails, db: Session = Depends(get_db)):
    token = views.login_user(user_details, db)
    return token


@auth_router.post("/refresh/", response_model=Token)
def refresh_token(token_details: RefreshDetails, db: Session = Depends(get_db)):
    tokens = views.refresh_token(token_details, db)
    return tokens


@auth_router.get("/me/", response_model=UserOut)
def get_user_profile(current_user: UserOut = Depends(get_active_user)):
    return current_user
