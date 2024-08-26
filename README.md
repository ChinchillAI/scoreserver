Generate DB Migrations:
alembic revision --autogenerate -m "Some description"

Apply Migrations:
alembic upgrade head

Run App:
uvicorn scoreserver.main:app

