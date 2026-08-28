from celery import shared_task

from dependencies.dragonfly import DragonflyDep, with_dragonfly


@with_dragonfly
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
        return run_dragonfly_check()
    except Exception as e:
        print(f"[X] Error al conectar o interactuar con Dragonfly: {e}")
