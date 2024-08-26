from fastapi import APIRouter
from typing import Any
from sqlmodel import select
from ..deps import SessionDep
from ...models import HighScore


router = APIRouter()


@router.get("/")
def read_highscores(session: SessionDep) -> Any:  # pyright: ignore[reportAny]
    return session.exec(select(HighScore)).all()
