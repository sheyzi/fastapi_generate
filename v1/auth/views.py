from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session

from core.auth import auth
from core.mail import send_mail
from models.users import User
from schemas.users import UserCreate
from schemas.auth import LoginDetails, RefreshDetails, Token, EmailSchema


def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user


def create_user(user_details: UserCreate, db: Session):
    user_details.email = user_details.email.lower()
    old_user = get_user_by_email(email=user_details.email, db=db)
    if old_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            "User with this email already exists")
    user_details_dict = user_details.dict()
    del user_details_dict['password']
    new_user = User(
        **user_details_dict,
        password=auth.hash_password(user_details.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login_user(user_details: LoginDetails, db: Session):
    user_details.email = user_details.email.lower()
    user = get_user_by_email(email=user_details.email, db=db)
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


def send_test_mail(background_tasks: BackgroundTasks, emails: EmailSchema):
    send_mail(background_tasks=background_tasks, subject="Test Mail",
              emails=emails, template_name="test_email.html")
    return {"msg": "Success"}
