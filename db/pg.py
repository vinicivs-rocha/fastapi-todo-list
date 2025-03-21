import os
from typing import Annotated

from alembic import command
from alembic.config import Config
from fastapi import Depends
from sqlmodel import create_engine, Session


def get_engine():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    return create_engine(database_url)


def get_session():
    with Session(get_engine()) as session:
        yield session


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "heads")


SessionDep = Annotated[Session, Depends(get_session)]

if __name__ == "__main__":
    run_migrations()
