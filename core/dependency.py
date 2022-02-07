from fastapi import Security, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from models.users import User
from schemas.users import UserOut
from core.database import SessionLocal
from core.auth import auth

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    email = auth.decode_token(token)
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(401, "User doesn't exist")
    return user


def get_active_user(current_user: UserOut = Depends(get_user)):
    if not current_user.is_active:
        raise HTTPException("This account is inactive!")
    return current_user
