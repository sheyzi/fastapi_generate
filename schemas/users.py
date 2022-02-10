from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    email_verified: bool
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True
