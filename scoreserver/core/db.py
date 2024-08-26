from sqlmodel import create_engine
from .config import settings
from ..models import User, HighScore  # pyright: ignore[reportUnusedImport]


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
