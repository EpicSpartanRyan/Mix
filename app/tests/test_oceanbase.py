import os
import time
from urllib.parse import quote_plus

import pymysql
from celery import shared_task
from sqlmodel import Field, SQLModel, create_engine

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


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@shared_task
def test_oceanbase_connection():
    print(f"Esperando a que OceanBase esté listo en {OB_HOST}:{OB_PORT}...")
    
    max_retries = 30
    delay = 3
    
    for attempt in range(1, max_retries + 1):
        try:
            connection = pymysql.connect(
                host=OB_HOST,
                port=OB_PORT,
                user=OB_USER,
                password=OB_PASSWORD,
                database="oceanbase",
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=5
            )
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT version() as version;")
                result = cursor.fetchone()
                print("¡Conexión a OceanBase exitosa!")
                print(f"Versión del motor: {result['version']}")

            create_db_and_tables()
            print("Tabla users creada o ya existente.")
            connection.close()
            return {
                "host": OB_HOST,
                "port": OB_PORT,
                "database": OB_DATABASE,
                "table": "users",
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