import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Predictor de Depósitos Bancarios", page_icon="🏦")
st.title("🏦 Predicción de Suscripción a Depósito a Plazo")
st.write("Estimación previa a la llamada comercial (sin fuga de datos).")

modelo = joblib.load("app/modelo.joblib")

col1, col2 = st.columns(2)
with col1:
    edad = st.slider("Edad", 18, 95, 42)
    saldo = st.number_input("Saldo promedio anual (€)", -8000, 100000, 1200)
    hipoteca = st.selectbox("¿Tiene hipoteca?", [0, 1], format_func=lambda x: "Sí" if x == 1 else "No")
    prestamo = st.selectbox("¿Tiene préstamo personal?", [0, 1], format_func=lambda x: "Sí" if x == 1 else "No")
    moroso = st.selectbox("¿Tiene crédito en mora?", [0, 1], format_func=lambda x: "Sí" if x == 1 else "No")
    trabajo = st.selectbox("Ocupación", ["management", "technician", "blue-collar", "admin.", "services", "retired", "student", "self-employed", "unemployed", "entrepreneur", "housemaid", "unknown"])
    estado_civil = st.selectbox("Estado civil", ["married", "single", "divorced"])

with col2:
    educacion = st.selectbox("Nivel educativo", ["tertiary", "secondary", "primary", "unknown"])
    contacto = st.selectbox("Canal de contacto", ["cellular", "telephone", "unknown"])
    mes = st.selectbox("Mes de contacto", ["may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "jan", "feb", "mar", "apr"])
    dia = st.slider("Día del mes", 1, 31, 15)
    campana = st.number_input("Contactos en esta campaña", 1, 50, 1)
    dias_previos = st.number_input("Días desde campaña previa (-1 = nunca)", -1, 900, -1)
    contactos_previos = st.number_input("Contactos previos", 0, 50, 0)
    resultado_previo = st.selectbox("Resultado campaña previa", ["unknown", "failure", "other", "success"])

if st.button("Predecir propensión", type="primary"):
    fila = pd.DataFrame([{
        "edad": edad, "moroso": moroso, "saldo": saldo, "hipoteca": hipoteca,
        "prestamo": prestamo, "dia": dia, "campana": campana,
        "dias_previos": dias_previos, "contactos_previos": contactos_previos,
        "trabajo": trabajo, "estado_civil": estado_civil, "educacion": educacion,
        "contacto": contacto, "mes": mes, "resultado_previo": resultado_previo
    }])
    prob = modelo.predict_proba(fila)[0, 1]
    pred = modelo.predict(fila)[0]
    st.metric("Probabilidad de suscripción", f"{prob:.1%}")
    if pred == 1:
        st.success("✅ **Cliente prioritario:** alta propensión a contratar depósito a plazo.")
    else:
        st.info("ℹ️ **Baja prioridad:** menor probabilidad de conversión en esta campaña.")
