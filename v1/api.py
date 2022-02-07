from fastapi import APIRouter
from .auth.routes import auth_router

api_router = APIRouter(prefix="/v1")

api_router.include_router(auth_router)
