from database import get_connection


def procesar_lectura(data):
    print("Procesando lectura...")

    sensor_id = data.get("sensor_id")
    zona_id = data.get("zona_id")
    ph = data.get("ph")
    turbidez = data.get("turbidez")
    temperatura = data.get("temperatura")

    guardar_lectura(zona_id, sensor_id, ph, turbidez, temperatura)


def guardar_lectura(zona_id, sensor_id, ph, turbidez, temperatura):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO lecturas (
        zona_id,
        sensor_codigo,
        ph,
        turbidez,
        temperatura
    )
    VALUES (%s, %s, %s, %s, %s);
    """

    cursor.execute(query, (zona_id, sensor_id, ph, turbidez, temperatura))

    conn.commit()
    cursor.close()
    conn.close()

    print("Lectura guardada en PostgreSQL")