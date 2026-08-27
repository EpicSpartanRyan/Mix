import os
import time
from typing import Annotated
from urllib.parse import quote_plus

from celery import shared_task
from fastapi import Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select

OB_HOST = os.getenv("OB_HOST", "oceanbase")
OB_PORT = int(os.getenv("OB_PORT", 2881))
OB_USER = os.getenv("OB_USER", "root@sys")
OB_PASSWORD = os.getenv("OB_PASSWORD", "")
OB_DATABASE = os.getenv("OB_DATABASE", "oceanbase")


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str


DATABASE_URL = (
    f"mysql+pymysql://{quote_plus(OB_USER)}:{quote_plus(OB_PASSWORD)}"
    f"@{OB_HOST}:{OB_PORT}/{OB_DATABASE}?charset=utf8mb4"
)
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_and_find_test_user(session: SessionDep):
    user_suffix = int(time.time())
    user_to_create = User(
        username=f"test_user_{user_suffix}",
        email=f"test_user_{user_suffix}@example.com",
        password="test-password",
    )

    session.add(user_to_create)
    session.commit()
    session.refresh(user_to_create)

    statement = select(User).where(User.username == user_to_create.username)
    user_found = session.exec(statement).first()

    if user_found is None:
        raise RuntimeError("El usuario de prueba no fue encontrado.")

    return user_found


@shared_task
def test_oceanbase_connection():
    print(f"Esperando a que OceanBase esté listo en {OB_HOST}:{OB_PORT}...")

    max_retries = 30
    delay = 3

    for attempt in range(1, max_retries + 1):
        try:
            create_db_and_tables()
            with Session(engine) as session:
                user_found = create_and_find_test_user(session)
            print("¡Conexión a OceanBase exitosa!")
            print(f"Usuario creado y encontrado: {user_found.username} (id={user_found.id})")
            return {
                "host": OB_HOST,
                "port": OB_PORT,
                "database": OB_DATABASE,
                "table": "users",
                "user": {
                    "id": user_found.id,
                    "username": user_found.username,
                    "email": user_found.email,
                },
                "status": "¡Conexión y tabla users verificadas con éxito!"
            }
        except Exception as e:
            print(f"Intento {attempt}/{max_retries} fallido: El motor aún está iniciando. Reintentando en {delay}s...")
            time.sleep(delay)
            
    return {
        "host": OB_HOST,
        "port": OB_PORT,
        "status": "Error: No se pudo establecer la conexión con OceanBase."
    }