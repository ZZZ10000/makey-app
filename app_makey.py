import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Makey E.I.R.L. - Predictor Energético Corfo",
    page_icon="☀️",
    layout="wide"
)

# --- ESTILOS UX/UI MEJORADOS PARA CONTRASTE ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    
    /* Estilo para las tarjetas de métricas con alto contraste */
    [data-testid="stMetricValue"] {
        color: #000000 !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricLabel"] {
        color: #333333 !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 2px solid #1B5E20;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.1);
    }
    
    h1, h2, h3 { color: #1B5E20; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stSlider [data-baseweb="slider"] { margin-bottom: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL (DATOS Y CONFIGURACIÓN) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3106/3106856.png", width=100)
    st.title("Makey E.I.R.L.")
    st.subheader("Simulador Predictivo")
    
    st.markdown("### Parámetros del Proyecto")
    costo_mensual_actual = st.slider("Gasto Mensual Actual (CLP)", 100000, 2000000, 500000, step=50000)
    incremento_energia = st.slider("Inflación Energética Anual (%)", 2.0, 15.0, 5.0)
    costo_sistema_total = st.number_input("Costo Total del Sistema (CLP)", value=15000000)
    
    st.divider()
    st.markdown("**Equipo de Gestión:**")
    st.info(f"👤 **José Eyzaguirre**\n📞 +569 5809 4386\n\n👤 **Víctor Pulgar**\n📞 +569 6786 7844")

# --- CUERPO PRINCIPAL ---
st.title("☀️ Simulador de Inversión y Proyección de Utilidades")
st.markdown("### Análisis Financiero Inteligente: Implementación ERNC con Subsidio Corfo")

# --- LÓGICA PREDICTIVA ---
# Cálculo de Subsidio (60% Corfo)
subsidio_corfo = costo_sistema_total * 0.60
inversion_agricultor = costo_sistema_total * 0.40
ahorro_estimado_porcentaje = 0.90 # 90% de ahorro

# Generación de Proyección a 10 años
años = np.array(range(0, 11)).reshape(-1, 1)
flujo_tradicional = []
flujo_solar = []
utilidad_acumulada = []

gasto_acumulado_tradicional = 0
gasto_acumulado_solar = inversion_agricultor # Empezamos con el costo inicial del 40%

for i in range(11):
    # Inflación aplicada al costo de energía
    costo_ajustado = costo_mensual_actual * 12 * ((1 + (incremento_energia/100)) ** i)
    
    # Escenario Tradicional
    gasto_acumulado_tradicional += costo_ajustado
    flujo_tradicional.append(gasto_acumulado_tradicional)
    
    # Escenario Solar (Ahorro del 90%)
    costo_solar_anual = costo_ajustado * (1 - ahorro_estimado_porcentaje)
    gasto_acumulado_solar += costo_solar_anual
    flujo_solar.append(gasto_acumulado_solar)
    
    # Utilidad neta (Diferencia entre no hacer nada y hacer el proyecto)
    utilidad_acumulada.append(gasto_acumulado_tradicional - gasto_acumulado_solar)

# --- VISUALIZACIÓN DE MÉTRICAS CON MEJOR CONTRASTE ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Subsidio Corfo (60%)", f"${subsidio_corfo:,.0f}")
col2.metric("Su Inversión (40%)", f"${inversion_agricultor:,.0f}")
col3.metric("Ahorro Año 1", f"${(costo_mensual_actual * 12 * ahorro_estimado_porcentaje):,.0f}")

# Cálculo de Payback (Punto de equilibrio)
años_payback = inversion_agricultor / (costo_mensual_actual * 12 * ahorro_estimado_porcentaje)
col4.metric("Retorno de Inversión", f"{años_payback:.1f} Años", delta="Punto de Equilibrio", delta_color="normal")

st.divider()

# --- GRÁFICOS INTERACTIVOS ---
tab1, tab2 = st.tabs(["📊 Proyección de Ahorro", "💰 Utilidad Acumulada (Predicción)"])

with tab1:
    st.subheader("Comparativa de Gasto Acumulado (10 Años)")
    df_proyeccion = pd.DataFrame({
        "Año": list(range(11)) * 2,
        "Gasto Acumulado (CLP)": flujo_tradicional + flujo_solar,
        "Sistema": ["Tradicional (Sin Corfo)"] * 11 + ["Solar (Makey + Corfo)"] * 11
    })
    
    fig_line = px.line(df_proyeccion, x="Año", y="Gasto Acumulado (CLP)", color="Sistema",
                       markers=True, line_shape="spline",
                       color_discrete_map={"Tradicional (Sin Corfo)": "#d32f2f", "Solar (Makey + Corfo)": "#388e3c"})
    st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    st.subheader("Predicción de Utilidades Generadas")
    st.write("Esta gráfica muestra el dinero que permanece en su bolsillo gracias al cambio a energía solar.")
    
    df_utilidad = pd.DataFrame({
        "Año": list(range(11)),
        "Utilidad Acumulada (CLP)": utilidad_acumulada
    })
    
    fig_area = px.area(df_utilidad, x="Año", y="Utilidad Acumulada (CLP)",
                       title="Crecimiento de Capital Neto (Ahorro Reinvertido)",
                       color_discrete_sequence=["#66bb6a"])
    st.plotly_chart(fig_area, use_container_width=True)

# --- SECCIÓN DE REQUISITOS CRÍTICOS ---
st.divider()
st.header("📌 Factores Críticos de Éxito")
c1, c2 = st.columns(2)

with c1:
    st.markdown(f"""
    ### 📁 Carpeta Tributaria
    El motor de la postulación. **José Eyzaguirre** analizará su historial para asegurar:
    * **Impacto Económico:** Demostrar que el ahorro proyectado de **${utilidad_acumulada[-1]:,.0f}** a 10 años fortalecerá su empresa.
    * **Admisibilidad:** Verificación de ventas y cumplimiento tributario.
    """)

with c2:
    st.markdown(f"""
    ### ⚙️ Ingeniería y Gestión Técnica
    **Víctor Pulgar** se encarga de la precisión:
    * **Diseño Óptimo:** Ajuste de potencia para no sobredimensionar ni subestimar.
    * **Gestión de Financiamiento:** Asesoría técnica para que Corfo apruebe el 60% de los activos.
    """)

# --- BOTÓN DE ACCIÓN ---
if st.button("🚀 Iniciar Mi Evaluación Gratuita"):
    st.balloons()
    st.success("¡Excelente! José y Víctor han sido notificados. Prepare su Carpeta Tributaria para la revisión.")

st.caption("© 2026 Makey E.I.R.L. - Los cálculos son proyecciones basadas en algoritmos de crecimiento lineal e inflación estimada.")