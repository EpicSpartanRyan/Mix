import redis
from celery import shared_task

# Como el script corre dentro de Docker (o puedes cambiarlo a 'localhost' si lo corres directo en tu máquina)
# Si lo pruebas desde fuera de Docker usa 'localhost', si está dentro de la red del compose usa 'dragonfly'


@shared_task
def test_dragonfly_connection():

    HOST = "dragonfly"
    PORT = 6379
    try:
        # Inicializar cliente de Redis (Dragonfly es 100% compatible con el protocolo Redis)
        r = redis.Redis(host=HOST, port=PORT, decode_responses=True)
        
        # Probar ping
        if r.ping():
            print("[+] ¡Conexión exitosa a Dragonfly!")
            
        # Prueba de escritura
        key = "test_key"
        value = "¡Hola desde Dragonfly y Python!"
        r.set(key, value)

        # Prueba de lectura
        retrieved_value = r.get(key)
        r.delete(key)

        return {
            "redis_version": redis.__version__,
            "value": retrieved_value,
            "status": "¡Cache dragonfly probada con exito!"
        }
        
    except Exception as e:
        print(f"[X] Error al conectar o interactuar con Dragonfly: {e}")
