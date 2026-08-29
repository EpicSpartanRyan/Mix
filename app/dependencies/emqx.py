import os
import time
from contextlib import contextmanager
from functools import wraps
from typing import Annotated

import paho.mqtt.client as mqtt
from fastapi import Depends

BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "emqx")
BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "python_test_script")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "iot/test/conexion")
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE", 60))
MQTT_MAX_RETRIES = int(os.getenv("MQTT_MAX_RETRIES", 5))
MQTT_RETRY_DELAY = float(os.getenv("MQTT_RETRY_DELAY", 3))
MQTT_STARTUP_DELAY = float(os.getenv("MQTT_STARTUP_DELAY", 1))
MQTT_MESSAGE_DELAY = float(os.getenv("MQTT_MESSAGE_DELAY", 2))
TOPIC_PRUEBA = MQTT_TOPIC


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"[+] Conectado exitosamente al broker EMQX (Código: {reason_code})")
        client.subscribe(TOPIC_PRUEBA)
        print(f"[+] Suscrito al tópico: {TOPIC_PRUEBA}")
    else:
        print(f"[-] Error de conexión. Código de razón: {reason_code}")


def on_message(client, userdata, msg):
    print(f"\n[📩 MENSAJE RECIBIDO]")
    print(f"   -> Tópico   : {msg.topic}")
    print(f"   -> Payload  : {msg.payload.decode('utf-8')}")


def on_subscribe(client, userdata, mid, reason_codes, properties):
    print(f"[+] Suscripción confirmada (MID: {mid})")


@contextmanager
def emqx_context():
    client = mqtt.Client(
        client_id=MQTT_CLIENT_ID,
        protocol=mqtt.MQTTv5,
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    )
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe

    for attempt in range(MQTT_MAX_RETRIES):
        try:
            client.connect(BROKER_HOST, BROKER_PORT, keepalive=MQTT_KEEPALIVE)
            client.loop_start()
            time.sleep(MQTT_STARTUP_DELAY)
            try:
                yield client
            finally:
                client.loop_stop()
                client.disconnect()
            return
        except Exception:
            if attempt == MQTT_MAX_RETRIES - 1:
                raise
            time.sleep(MQTT_RETRY_DELAY)

# For celery tasks, we need a way to get a session without using Depends.
def with_emqx(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        with emqx_context() as client:
            return function(client, *args, **kwargs)

    return wrapper


def get_emqx():
    with emqx_context() as client:
        yield client

# For FastAPI routes, we can use Depends to inject the session.
EmqxDep = Annotated[mqtt.Client, Depends(get_emqx)]
