from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from paho.mqtt import client as mqtt_client
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

broker = "35.193.246.15"
port = 1883
topic = "hospital/camas_407"
client_id = f'fastapi-mqtt-{random.randint(0, 1000)}'

mqtt = mqtt_client.Client(
    client_id=client_id,
    protocol=mqtt_client.MQTTv311
)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT!")
    else:
        print(f"Falló la conexión, código de error: {rc}")

mqtt.on_connect = on_connect

def connect_mqtt():
    mqtt.connect(broker, port)
    mqtt.loop_start()

connect_mqtt()

@app.get("/")
async def serve_index():
    return FileResponse("index.html")

@app.post("/enviar/{evento}")
async def enviar_evento(evento: str):
    mqtt.publish(topic, f'{{"status": "{evento}"}}')
    return {"status": "success", "evento": evento}
