import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000/lecturas"

st.set_page_config(
    page_title="AquaSense IA",
    page_icon="",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0f172a;
        color: white;
    }

    [data-testid="stHeader"] {
        background-color: #0f172a;
    }

    h1, h2, h3, h4, p, label {
        color: #f9fafb !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def estado_parametro(valor, minimo, maximo):
    if valor < minimo:
        return "Bajo", "#2563eb"
    elif valor > maximo:
        return "Alto", "#dc2626"
    else:
        return "Normal", "#16a34a"


def tarjeta_parametro(nombre, valor, unidad, minimo, maximo):
    estado, color = estado_parametro(valor, minimo, maximo)

    st.markdown(
        f"""
        <div style="
            background-color:#111827;
            padding:22px;
            border-radius:16px;
            border-left:8px solid {color};
            box-shadow:0 4px 12px rgba(0,0,0,0.25);
        ">
            <h4 style="color:#d1d5db; margin:0;">{nombre}</h4>
            <h1 style="color:{color}; margin:8px 0;">{valor} {unidad}</h1>
            <p style="color:#9ca3af; margin:0;">Estado: {estado}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


st.title("AquaSense IA")
st.subheader("Dashboard de monitoreo de calidad del agua")

try:
    response = requests.get(API_URL)
    data = response.json()

    if not data:
        st.warning("No hay lecturas registradas todavía.")
    else:
        df = pd.DataFrame(data)
        df["fecha"] = pd.to_datetime(df["fecha"])

        ultima = df.iloc[0]

        col1, col2, col3 = st.columns(3)

        with col1:
            tarjeta_parametro("pH", ultima["ph"], "", 6.5, 8.5)

        with col2:
            tarjeta_parametro("Turbidez", ultima["turbidez"], "NTU", 0, 100)

        with col3:
            tarjeta_parametro("Temperatura", ultima["temperatura"], "°C", 20, 30)

        st.divider()

        estado = "Normal"
        recomendacion = "El agua se encuentra dentro de condiciones aceptables."

        if ultima["ph"] < 6.5:
            estado = "Advertencia"
            recomendacion = "El pH está bajo. Se recomienda revisar posible acidez en el agua."
        elif ultima["ph"] > 8.5:
            estado = "Advertencia"
            recomendacion = "El pH está alto. Se recomienda verificar alcalinidad o tratamiento del agua."

        if ultima["turbidez"] > 100:
            estado = "Crítico"
            recomendacion = "La turbidez es alta. Se recomienda evitar el uso del agua hasta realizar revisión."

        st.info(f"Estado general: {estado}")
        st.success(f"Recomendación: {recomendacion}")

        st.divider()

        st.subheader("Histórico de lecturas")

        df_ordenado = df.sort_values("fecha")

        fig_ph = px.line(df_ordenado, x="fecha", y="ph", title="Variación del pH")
        st.plotly_chart(fig_ph, use_container_width=True)

        fig_turbidez = px.line(df_ordenado, x="fecha", y="turbidez", title="Variación de turbidez")
        st.plotly_chart(fig_turbidez, use_container_width=True)

        fig_temp = px.line(df_ordenado, x="fecha", y="temperatura", title="Variación de temperatura")
        st.plotly_chart(fig_temp, use_container_width=True)

        st.subheader("Últimas lecturas")

        tabla = df[[
            "fecha",
            "ph",
            "turbidez",
            "temperatura"
        ]]

        st.dataframe(
            tabla.sort_values("fecha", ascending=False),
            use_container_width=True
        )

except Exception as e:
    st.error("No se pudo conectar con la API.")
    st.write(e)