import time

from celery import shared_task

from dependencies.emqx import BROKER_HOST, EmqxDep, TOPIC_PRUEBA, emqx_context

def run_emqx_check(client: EmqxDep):
    time.sleep(1)
    mensaje_payload = "¡Hola EMQX desde Python y PyTorch Stack!"
    print(f"[*] Publicando mensaje en '{TOPIC_PRUEBA}'...")

    result = client.publish(TOPIC_PRUEBA, mensaje_payload, qos=1)
    result.wait_for_publish()
    print("[+] Mensaje publicado correctamente.")
    time.sleep(2)

    return {
        "broker_host": BROKER_HOST,
        "topic": TOPIC_PRUEBA,
        "status": "¡Prueba EMQX completada con éxito!"
    }


@shared_task
def test_emqx_connection():
    print("[*] Inicializando cliente MQTT...")
    try:
        with emqx_context() as client:
            result = run_emqx_check(client)
        print("[+] Prueba finalizada con éxito.")
        return result
    except Exception as error:
        print(f"[X] Error al conectar o interactuar con EMQX: {error}")
        return {"status": "Error: No se pudo conectar a EMQX."}