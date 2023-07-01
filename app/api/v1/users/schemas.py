import uuid
from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserUpdate(UserBase):
    pass


class UserCreate(UserBase):
    password: str

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@company.com",
                "password": "secret",
            }
        }


class UserRead(UserBase):
    id: uuid.UUID
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@company.com",
                "is_active": True,
                "is_superuser": False,
            }
        }
