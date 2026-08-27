from celery import shared_task

from dependencies.dragonfly import DragonflyDep, dragonfly_context


def run_dragonfly_check(client: DragonflyDep):
    if client.ping():
        print("[+] ¡Conexión exitosa a Dragonfly!")

    key = "test_key"
    value = "¡Hola desde Dragonfly y Python!"
    client.set(key, value)
    retrieved_value = client.get(key)
    redis_version = client.info().get("redis_version")
    client.delete(key)

    return {
        "redis_version": redis_version,
        "value": retrieved_value,
        "status": "¡Cache dragonfly probada con exito!"
    }


@shared_task
def test_dragonfly_connection():
    try:
        with dragonfly_context() as client:
            return run_dragonfly_check(client)
    except Exception as e:
        print(f"[X] Error al conectar o interactuar con Dragonfly: {e}")
