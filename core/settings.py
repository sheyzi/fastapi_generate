from pydantic import BaseModel
from decouple import config


class Settings(BaseModel):
    PROJECT_TITLE: str = 'FastAPI Auth'
    PROJECT_VERSION: str = '1.0.0'

    DETA_PROJECT_KEY: str = config("DETA_PROJECT_KEY")
    DETA_PROJECT_ID: str = config("DETA_PROJECT_ID")

    MAIL_USERNAME: str = config("MAIL_USERNAME")
    MAIL_PASSWORD: str = config("MAIL_PASSWORD")
    MAIL_FROM: str = config("MAIL_FROM")
    MAIL_PORT: str = config("MAIL_PORT")
    MAIL_SERVER: str = config("MAIL_SERVER")

    DATABASE_USER: str = config("POSTGRES_USER")
    DATABASE_PASSWORD: str = config("POSTGRES_PASSWORD")
    DATABASE_SERVER: str = config("POSTGRES_SERVER")
    DATABASE_PORT: str = config("POSTGRES_PORT")
    DATABASE_NAME: str = config("POSTGRES_DB")
    DATABASE_URL: str = f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_SERVER}:{DATABASE_PORT}/{DATABASE_NAME}"

    SECRET_KEY: str = config("SECRET")
    ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRY_SECONDS: int = 900
    REFRESH_TOKEN_EXPIRY_DAYS: int = 30
    EMAIL_TOKEN_EXPIRY_MINUTES: int = 30
    RESET_TOKEN_EXPIRY_MINUTES: int = 30

    FRONTEND_URL: str = config("FRONTEND_URL", default=None)


settings = Settings()
