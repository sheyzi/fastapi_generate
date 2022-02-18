from fastapi import APIRouter, BackgroundTasks, Depends, Request, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session

from core.dependency import get_db, get_active_user
from schemas.users import UserCreate, UserOut
from schemas.auth import RefreshDetails, Token, LoginDetails, ResetPasswordDetails

from . import views

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/register/", response_model=UserOut, status_code=201)
def register_user(request: Request, background_tasks: BackgroundTasks, user_details: UserCreate,
                  db: Session = Depends(get_db)):
    user = views.create_user(user_details, db, background_tasks, request)
    return user


@auth_router.post("/login/", response_model=Token)
def login(*, user_details: LoginDetails, db: Session = Depends(get_db), bg_tasks: BackgroundTasks, request: Request):
    token = views.login_user(user_details, db, bg_tasks, request)
    return token


@auth_router.post("/refresh/", response_model=Token)
def refresh_token(token_details: RefreshDetails, db: Session = Depends(get_db)):
    tokens = views.refresh_token(token_details, db)
    return tokens


@auth_router.get("/me/", response_model=UserOut)
def get_user_profile(current_user: UserOut = Depends(get_active_user)):
    """
     Get active user's profile
     """
    return current_user


@auth_router.get("/email-verify/")
def verify_email(token: str, db: Session = Depends(get_db)):
    response = views.verify_email(token, db)
    return response


@auth_router.get("/email-verify-resend/")
def resend_verification_email(email: EmailStr, background_tasks: BackgroundTasks, requests: Request,
                              db: Session = Depends(get_db)):
    response = views.resend_verification_email(
        email, background_tasks, requests, db)
    return response


@auth_router.get("/reset-password/")
def reset_password(email: EmailStr, bg_tasks: BackgroundTasks, requests: Request, db: Session = Depends(get_db)):
    done = views.reset_password(email, bg_tasks, requests, db)
    if not done:
        raise HTTPException(500, "There was an error processing your request!")
    return {"msg": "Reset email sent"}


@auth_router.post("/reset-password-confirm/")
def rest_password_confirm(body: ResetPasswordDetails, bg_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db) ):
    done = views.reset_password_verification(body, request, bg_tasks, db)
    if not done:
        raise HTTPException(500, "There was an error processing your request!")
    return {"msg": "Password reset successful"}

