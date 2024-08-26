from fastapi import APIRouter
from .routes import users, high_scores


api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(high_scores.router, prefix="/scores", tags=["highscores"])
