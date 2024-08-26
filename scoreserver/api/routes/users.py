from typing import Any
from fastapi import APIRouter
from sqlmodel import select
from ..deps import SessionDep
from ...models import User


router = APIRouter()


@router.get("/")
def read_users(session: SessionDep) -> Any:  # pyright: ignore[reportAny]
    return session.exec(select(User)).all()
