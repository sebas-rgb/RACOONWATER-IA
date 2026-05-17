from fastapi import FastAPI

from app.mqtt.costumer import iniciar_mqtt
from app.routes.lecturas_routes import router as lecturas_router

app = FastAPI()

mqtt_client = None


# =========================================
# INICIO BACKEND
# =========================================

@app.on_event("startup")
def startup_event():

    global mqtt_client

    mqtt_client = iniciar_mqtt()

    print("MQTT iniciado")


# =========================================
# RUTAS
# =========================================

app.include_router(lecturas_router)


@app.get("/")
def root():
    return {"mensaje": "AquaSense IA funcionando"}