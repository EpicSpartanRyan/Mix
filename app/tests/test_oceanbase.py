import os
import time
import pymysql
from celery import shared_task

OB_HOST = os.getenv("OB_HOST", "oceanbase")
OB_PORT = int(os.getenv("OB_PORT", 2881))
OB_USER = "root@sys"
OB_PASSWORD = ""

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
                
            connection.close()
            return {
                "host": OB_HOST,
                "port": OB_PORT,
                "database": "oceanbase",
                "status": "¡Prueba OceanBase completada con éxito!"
            }
        except Exception as e:
            print(f"Intento {attempt}/{max_retries} fallido: El motor aún está iniciando. Reintentando en {delay}s...")
            time.sleep(delay)
            
    return {
        "host": OB_HOST,
        "port": OB_PORT,
        "status": "Error: No se pudo establecer la conexión con OceanBase."
    }