from pydantic import BaseModel
from decouple import config


class Settings(BaseModel):
    PROJECT_TITLE: str = 'Ecommerce API'
    PROJECT_VERSION: str = '1.0.0'

    DETA_PROJECT_KEY: str = config("DETA_PROJECT_KEY")
    DETA_PROJECT_ID: str = config("DETA_PROJECT_ID")

    DATABASE_USER: str = config("POSTGRES_USER")
    DATABASE_PASSWORD: str = config("POSTGRES_PASSWORD")
    DATABASE_SERVER: str = config("POSTGRES_SERVER")
    DATABASE_PORT: str = config("POSTGRES_PORT")
    DATABASE_NAME: str = config("POSTGRES_DB")
    DATABASE_URL: str = f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_SERVER}:{DATABASE_PORT}/{DATABASE_NAME}"

    SECRET_KEY: str = config("SECRET")
    ALGORITHM = "HS256"

    # ACCESS_TOKEN_EXPIRY_SECONDS: int = 5
    ACCESS_TOKEN_EXPIRY_SECONDS: int = 900
    REFRESH_TOKEN_EXPIRY_DAYS: int = 30


settings = Settings()
