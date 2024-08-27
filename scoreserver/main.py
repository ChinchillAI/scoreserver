from fastapi import FastAPI
from .api.main import api_router
from .core.config import settings

print(f"database uri: {settings.SQLALCHEMY_DATABASE_URI}")
app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
