def generar_recomendacion(ph, turbidez, temperatura):
    estado = "Normal"
    recomendaciones = []

    if ph < 6.5:
        estado = "Advertencia"
        recomendaciones.append("El pH está bajo. Se recomienda revisar posible acidez del agua.")

    elif ph > 8.5:
        estado = "Advertencia"
        recomendaciones.append("El pH está alto. Se recomienda revisar posible alcalinidad o exceso de químicos.")

    if turbidez > 100:
        estado = "Crítico"
        recomendaciones.append("La turbidez es alta. Se recomienda evitar el uso del agua y revisar filtración.")

    if temperatura < 20:
        recomendaciones.append("La temperatura está baja. Se recomienda verificar condiciones del entorno.")

    elif temperatura > 30:
        recomendaciones.append("La temperatura está alta. Se recomienda revisar exposición al sol o contaminación térmica.")

    if not recomendaciones:
        recomendaciones.append("El agua se encuentra dentro de los parámetros aceptables.")

    return {
        "estado": estado,
        "recomendacion": " ".join(recomendaciones)
    }