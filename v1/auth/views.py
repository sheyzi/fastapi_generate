from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.auth import auth
from models.users import User
from schemas.users import UserCreate
from schemas.auth import LoginDetails, RefreshDetails, Token


def create_user(user_details: UserCreate, db: Session):
    old_user = db.query(User).filter(User.email == user_details.email).first()
    if old_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            "User with this email already exists")
    new_user = User(
        email=user_details.email,
        password=auth.hash_password(user_details.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login_user(user_details: LoginDetails, db: Session):
    user = db.query(User).filter(User.email == user_details.email).first()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            "User with this email doesn't exist!")
    if not auth.verify_password(user_details.password, user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            "Incorrect password!")

    access_token = auth.encode_token(user.email)
    refresh_token = auth.encode_refresh_token(user.email)
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


def refresh_token(token_details: RefreshDetails, db: Session):
    new_access_token, new_refresh_token = auth.refresh_token(
        token_details.refresh_token)
    return Token(access_token=new_access_token, refresh_token=new_refresh_token, token_type="bearer")
