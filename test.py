from database import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()

    print("Conexion exitosa a PostgreSQL\n")

    # Mostrar base actual
    cursor.execute("SELECT current_database();")
    db_name = cursor.fetchone()[0]

    print(f"Base de datos actual: {db_name}\n")

    # Mostrar tablas
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)

    tablas = cursor.fetchall()

    print("Tablas encontradas:\n")

    if tablas:
        for tabla in tablas:
            print(f"- {tabla[0]}")
    else:
        print("No hay tablas en la base de datos.")

    cursor.close()
    conn.close()

except Exception as e:
    print("Error:", e)