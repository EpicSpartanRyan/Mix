import os
import time

import paho.mqtt.client as mqtt
from celery import shared_task

# Leer la IP/Host desde el entorno (por defecto 'emqx' para Docker, o 'localhost' si lo corres fuera)
BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "emqx")
BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))
TOPIC_PRUEBA = "iot/test/conexion"

# Callbacks para la API moderna de paho-mqtt v2.x
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

@shared_task
def test_emqx_connection():
    print("[*] Inicializando cliente MQTT...")
    
    client = mqtt.Client(
        client_id="python_test_script", 
        protocol=mqtt.MQTTv5, 
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe

    print(f"[*] Intentando conectar a {BROKER_HOST}:{BROKER_PORT}...")
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

    client.loop_start()
    time.sleep(1)

    mensaje_payload = "¡Hola EMQX desde Python y PyTorch Stack!"
    print(f"[*] Publicando mensaje en '{TOPIC_PRUEBA}'...")
    
    result = client.publish(TOPIC_PRUEBA, mensaje_payload, qos=1)
    result.wait_for_publish()
    print("[+] Mensaje publicado correctamente.")

    time.sleep(2)
    client.loop_stop()
    client.disconnect()
    print("[+] Prueba finalizada con éxito.")

    return {
        "broker_host": BROKER_HOST,
        "topic": TOPIC_PRUEBA,
        "status": "¡Prueba EMQX completada con éxito!"
    }