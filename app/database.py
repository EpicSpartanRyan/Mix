import os
from contextlib import contextmanager
from typing import Annotated
from urllib.parse import quote_plus

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from models import User

OB_HOST = os.getenv("OB_HOST", "oceanbase")
OB_PORT = int(os.getenv("OB_PORT", 2881))
OB_USER = os.getenv("OB_USER", "root@sys")
OB_PASSWORD = os.getenv("OB_PASSWORD", "")
OB_DATABASE = os.getenv("OB_DATABASE", "oceanbase")

DATABASE_URL = (
    f"mysql+pymysql://{quote_plus(OB_USER)}:{quote_plus(OB_PASSWORD)}"
    f"@{OB_HOST}:{OB_PORT}/{OB_DATABASE}?charset=utf8mb4"
)
engine = create_engine(DATABASE_URL)


@contextmanager
def session_context():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def get_session():
    with session_context() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
