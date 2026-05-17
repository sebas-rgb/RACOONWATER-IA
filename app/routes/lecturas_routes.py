from fastapi import APIRouter
from database import get_connection

router = APIRouter()


# =========================================
# OBTENER ÚLTIMAS LECTURAS
# =========================================

@router.get("/lecturas")

def obtener_lecturas():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT
        id,
        zona_id,
        sensor_codigo,
        ph,
        turbidez,
        temperatura,
        fecha_lectura
    FROM lecturas
    ORDER BY fecha_lectura DESC
    LIMIT 20;
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    lecturas = []

    for row in rows:
        lecturas.append({
            "id": row[0],
            "zona_id": row[1],
            "sensor_codigo": row[2],
            "ph": float(row[3]),
            "turbidez": float(row[4]),
            "temperatura": float(row[5]),
            "fecha": row[6]
        })

    cursor.close()
    conn.close()

    return lecturas