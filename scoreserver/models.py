from sqlmodel import Relationship, SQLModel, Field  # pyright: ignore[reportUnknownVariableType]
import uuid


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    scores: list["HighScore"] = Relationship(
        back_populates="owner", cascade_delete=True
    )


class HighScore(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    score: int
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="scores")
