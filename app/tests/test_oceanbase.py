import time

from celery import shared_task
from sqlmodel import Session, select

from dependencies.database import (
    OB_DATABASE,
    OB_HOST,
    OB_PORT,
    with_session,
)
from models.user import User


@with_session
def create_and_find_test_user(session: Session):
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

    return {
        "id": user_found.id,
        "username": user_found.username,
        "email": user_found.email,
    }


@shared_task
def test_oceanbase_connection():
    print(f"Esperando a que OceanBase esté listo en {OB_HOST}:{OB_PORT}...")

    max_retries = 30
    delay = 3

    for attempt in range(1, max_retries + 1):
        try:
            user_found = create_and_find_test_user()
            print("¡Conexión a OceanBase exitosa!")
            print(f"Usuario creado y encontrado: {user_found['username']} (id={user_found['id']})")
            return {
                "host": OB_HOST,
                "port": OB_PORT,
                "database": OB_DATABASE,
                "table": "users",
                "user": {
                    "id": user_found["id"],
                    "username": user_found["username"],
                    "email": user_found["email"],
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