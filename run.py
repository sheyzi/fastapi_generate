import uvicorn

from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=settings.PORT, reload=settings.DEBUG
    )
