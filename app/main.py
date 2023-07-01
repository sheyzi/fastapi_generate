from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.core.config import settings
from app.api.deps import get_db
from app.api.v1.routes import router as v1_router
from app.db.init_db import init_db


def configure_router(app: FastAPI):
    app.include_router(
        v1_router,
        prefix=settings.API_V1_STR,
    )


def configure_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    configure_router(app)

    return app


app = configure_app()


@app.on_event("startup")
async def startup_event(db: Session = Depends(get_db)):
    init_db(db)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Hello World"}
