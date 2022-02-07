from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class LoginDetails(BaseModel):
    email: str
    password: str


class RefreshDetails(BaseModel):
    refresh_token: str
