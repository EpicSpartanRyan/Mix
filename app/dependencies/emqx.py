import os
import time
from contextlib import contextmanager
from typing import Annotated

import paho.mqtt.client as mqtt
from fastapi import Depends

BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "emqx")
BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))
TOPIC_PRUEBA = "iot/test/conexion"


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
        client_id="python_test_script",
        protocol=mqtt.MQTTv5,
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    )
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe

    for attempt in range(5):
        try:
            client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
            client.loop_start()
            time.sleep(1)
            try:
                yield client
            finally:
                client.loop_stop()
                client.disconnect()
            return
        except Exception:
            if attempt == 4:
                raise
            time.sleep(3)


def get_emqx():
    with emqx_context() as client:
        yield client


EmqxDep = Annotated[mqtt.Client, Depends(get_emqx)]
