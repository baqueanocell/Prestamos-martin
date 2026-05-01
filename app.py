import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configuración de nivel profesional
st.set_page_config(page_title="Martin Moreno - Gestión", layout="wide")

# Estilo personalizado (Dark Mode con acentos verdes)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1, h2, h3 { color: #00ffcc !important; }
    .stSlider > div > div > div > div { background: #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

def calcular_calendario(monto_total, cuotas, fecha_inicio, frecuencia):
    pagos = []
    monto_cuota = monto_total / cuotas
    fecha_actual = fecha_inicio
    for i in range(1, cuotas + 1):
        pagos.append({
            "N°": i,
            "Vencimiento": fecha_actual.strftime('%d/%m/%Y'),
            "Cobro": f"${round(monto_cuota, 2):,}"
        })
        if frecuencia == "Diario": fecha_actual += timedelta(days=1)
        elif frecuencia == "Semanal": fecha_actual += timedelta(weeks=1)
        else: fecha_actual += timedelta(days=30)
    return pagos

def main():
    st.title("🏦 Martin Moreno - Control de Préstamos")
    st.markdown("---")
    
    if 'db' not in st.session_state:
        st.session_state.db = []

    # Sidebar: Configuración Financiera
    with st.sidebar:
        st.header("⚙️ Configurar Préstamo")
        with st.form("registro_form", clear_on_submit=True):
            cliente = st.text_input("Nombre del Cliente")
            capital_base = st.number_input("Capital Prestado ($)", min_value=0.0, step=1000.0)
            
            # Selector de Interés solicitado (10% a 100%)
            tasa_interes = st.slider("Porcentaje de Interés (%)", 10, 100, 20)
            
            cuotas = st.number_input("Cantidad de Cuotas", min_value=1, step=1)
            frecuencia = st.selectbox("Ciclo de Cobro", ["Diario", "Semanal", "Mensual"])
            fecha = st.date_input("Fecha Inicio", datetime.now())
            
            # Cálculo interno
            monto_final = capital_base * (1 + (tasa_interes / 100))
            
            if st.form_submit_button("✅ Registrar en Agenda"):
                if cliente and capital_base > 0:
                    plan = calcular_calendario(monto_final, cuotas, fecha, frecuencia)
                    st.session_state.db.append({
                        "cliente": cliente, 
                        "plan": plan, 
                        "capital": capital_base,
                        "tasa": tasa_interes,
                        "total": monto_final,
                        "notas": ""
                    })
                    st.rerun()

    # Dashboard Principal
    if st.session_state.db:
        st.subheader("📋 Clientes Activos")
        for idx, item in enumerate(st.session_state.db):
            with st.expander(f"👤 {item['cliente']} | Total a Cobrar: ${item['total']:,} ({item['tasa']}% Int.)"):
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.write(f"**Capital Inicial:** ${item['capital']:,}")
                    st.write(f"**Interés Aplicado:** {item['tasa']}%")
                    st.dataframe(pd.DataFrame(item['plan']), hide_index=True)
                
                with col2:
                    st.subheader("📝 Ficha del Cliente")
                    nota_key = f"nota_{idx}"
                    st.session_state.db[idx]['notas'] = st.text_area(
                        "Datos de contacto / Notas de cobro:",
                        value=item['notas'],
                        key=nota_key,
                        height=150
                    )
                    if st.button("Guardar Cambios", key=f"btn_{idx}"):
                        st.success("Nota guardada correctamente.")
        
        if st.sidebar.button("🗑️ Borrar toda la base"):
            st.session_state.db = []
            st.rerun()
    else:
        st.info("Utiliza el panel lateral para ingresar el primer préstamo de Martin.")

if __name__ == "__main__":
    main()
