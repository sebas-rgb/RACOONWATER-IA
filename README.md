#  AquaSense IA

Sistema inteligente de monitoreo de calidad del agua basado en sensores IoT, mensajería MQTT, backend en Python, base de datos PostgreSQL y dashboard web.

---

##  Tecnologías utilizadas

- ESP32 simulado en Wokwi
- MQTT con HiveMQ Cloud
- Python
- FastAPI
- PostgreSQL
- Streamlit
- Pandas
- Plotly
- Paho MQTT
- Psycopg2
- Python Dotenv

---

##  Estructura del proyecto

```text
aquasense-backend/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   │
│   ├── mqtt/
│   │   └── consumer.py
│   │
│   ├── services/
│   │   ├── sensor_service.py
│   │   ├── analysis_service.py
│   │   ├── alert_service.py
│   │   └── ia_service.py
│   │
│   ├── repositories/
│   │   ├── lectura_repository.py
│   │   ├── alerta_repository.py
│   │   └── analisis_repository.py
│   │
│   ├── routes/
│   │   ├── lecturas_routes.py
│   │   ├── dashboard_routes.py
│   │   └── zonas_routes.py
│   │
│   └── schemas/
│       └── sensor_schema.py
│
├── dashboard/
│   └── dashboard.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

##  Flujo general del sistema

```text
ESP32/Wokwi
   ↓ MQTT
HiveMQ Cloud
   ↓
Python Consumer + FastAPI
   ↓
PostgreSQL
   ↓
Dashboard Streamlit
```

---

##  Requisitos previos

Antes de ejecutar el proyecto, debes tener instalado:

- Python 3.10 o superior
- PostgreSQL
- Visual Studio Code
- Cuenta gratuita en HiveMQ Cloud
- Proyecto ESP32 configurado en Wokwi

---

## 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/aquasense-ia.git
cd aquasense-ia
```

---

## 2. Crear entorno virtual

### Windows

```bash
python -m venv .venv
```

Activar entorno:

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 4. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto.

Ejemplo:

```env
# MQTT
MQTT_BROKER=tu_cluster.hivemq.cloud
MQTT_PORT=8883
MQTT_USER=ESP32
MQTT_PASSWORD=tu_password_mqtt
MQTT_TOPIC=aquasense/sensores/lecturas

# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=aquasense_ia
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_password_postgres
```

> El archivo `.env` no debe subirse a GitHub porque contiene credenciales privadas.

---

## 5. Crear base de datos en PostgreSQL

```sql
CREATE DATABASE aquasense_ia;
```

Luego ejecutar el script SQL del proyecto para crear las tablas necesarias.

Tablas principales:

- usuarios
- categorias_zona
- zonas_medicion
- sensores
- lecturas
- alertas
- recomendaciones
- eventos_mqtt

---

## 6. Insertar datos iniciales

Antes de recibir lecturas desde el ESP32, se debe crear al menos un usuario y una zona de medición.

```sql
INSERT INTO usuarios (nombre, correo, password_hash, rol)
VALUES ('Usuario Prueba', 'usuario@aquasense.com', '123456_hash', 'usuario');

INSERT INTO zonas_medicion (
    usuario_id,
    categoria_id,
    nombre,
    ubicacion,
    descripcion,
    tipo_uso
)
VALUES (
    1,
    1,
    'Zona de prueba Wokwi',
    'Simulación ESP32',
    'Zona creada para recibir datos simulados desde Wokwi',
    'educativo'
);
```

---

## 7. Probar conexión con PostgreSQL

```bash
python test.py
```

Resultado esperado:

```text
Conexion exitosa a PostgreSQL
```

---

## 8. Ejecutar backend FastAPI

```bash
uvicorn app.main:app --reload
```

API local:

```text
http://127.0.0.1:8000
```

Documentación automática:

```text
http://127.0.0.1:8000/docs
```

---

## 9. Ejecutar simulación en Wokwi

El ESP32 debe publicar mensajes al topic:

```text
aquasense/sensores/lecturas
```

Formato esperado:

```json
{
  "sensor_id": "sensor_001",
  "zona_id": 1,
  "ph": 7.2,
  "turbidez": 45.5,
  "temperatura": 24.8
}
```

Cuando el ESP32 publique datos, el backend debe mostrar:

```text
Conectado a HiveMQ
Suscrito al topic: aquasense/sensores/lecturas
Mensaje recibido...
Lectura guardada en PostgreSQL
```

---

## 10. Ejecutar dashboard

En otra terminal, con el entorno virtual activo:

```bash
streamlit run dashboard/dashboard.py
```

Dashboard local:

```text
http://localhost:8501
```

---

##  Funcionalidades del dashboard

El dashboard permite visualizar:

- Última lectura recibida
- Estado del pH
- Estado de turbidez
- Estado de temperatura
- Recomendación del sistema
- Gráficas históricas
- Tabla de últimas lecturas

---

##  Estados por color

| Color | Estado |
|---|---|
| Verde | Valor normal |
| Rojo | Valor por encima del rango |
| Azul | Valor por debajo del rango |

---

##  Recomendaciones inteligentes

El sistema genera recomendaciones básicas según los rangos definidos:

- pH menor a 6.5: posible acidez.
- pH mayor a 8.5: posible alcalinidad.
- Turbidez mayor a 100 NTU: posible contaminación o presencia de sedimentos.
- Temperatura menor a 20 °C o mayor a 30 °C: revisar condiciones del entorno.

---

##  Arquitectura aplicada

El proyecto aplica una arquitectura distribuida orientada a eventos:

- El ESP32 actúa como nodo IoT.
- HiveMQ Cloud funciona como broker MQTT.
- Python consume eventos de forma asíncrona.
- PostgreSQL almacena los datos de forma durable.
- FastAPI expone endpoints para consulta.
- Streamlit permite visualizar los datos en un dashboard web.

---

##  Comandos rápidos

Activar entorno virtual:

```bash
.venv\Scripts\activate
```

Ejecutar API:

```bash
uvicorn app.main:app --reload
```

Ejecutar dashboard:

```bash
streamlit run dashboard/dashboard.py
```

---

##  Estado del proyecto

Proyecto académico en desarrollo.

Actualmente cuenta con:

- Simulación ESP32 en Wokwi
- Envío MQTT a HiveMQ Cloud
- Consumidor Python
- Almacenamiento en PostgreSQL
- API con FastAPI
- Dashboard con Streamlit

---

##  Autor

Sebastian Lopez Alvarez  
Proyecto académico de Sistemas Distribuidos