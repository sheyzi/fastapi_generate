from fastapi import FastAPI

from models.base import Base
from core.database import engine
from core.settings import settings
from v1.api import api_router


def include_router(app: FastAPI):
    app.include_router(api_router)


def create_db():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
    include_router(app)
    create_db()
    return app


app = start_application()
