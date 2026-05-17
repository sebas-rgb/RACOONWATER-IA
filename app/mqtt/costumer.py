import json
import ssl
import paho.mqtt.client as mqtt

from config import (
    MQTT_BROKER,
    MQTT_PORT,
    MQTT_USER,
    MQTT_PASSWORD,
    MQTT_TOPIC
)

from app.services.sensor_service import procesar_lectura


# =========================================
# CALLBACK CONEXION
# =========================================

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado a HiveMQ")

        client.subscribe(MQTT_TOPIC)
        print(f"Suscrito al topic: {MQTT_TOPIC}")

    else:
        print(f"Error MQTT: {rc}")


# =========================================
# CALLBACK MENSAJES
# =========================================

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()

        print(f"Mensaje recibido: {payload}")

        data = json.loads(payload)

        procesar_lectura(data)

    except Exception as e:
        print("Error procesando mensaje:", e)


# =========================================
# INICIAR MQTT
# =========================================

def iniciar_mqtt():

    client = mqtt.Client()

    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.tls_insecure_set(True)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT)

    client.loop_start()

    return client