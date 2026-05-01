import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configuración profesional
st.set_page_config(page_title="Martin Moreno - Gestión", layout="wide", initial_sidebar_state="expanded")

# Estilo personalizado para que coincida con tu captura
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #00ffcc; font-family: 'Courier New', Courier, monospace; }
    </style>
    """, unsafe_allow_html=True)

def calcular_calendario(monto, cuotas, fecha_inicio, frecuencia):
    pagos = []
    monto_cuota = monto / cuotas
    fecha_actual = fecha_inicio
    for i in range(1, cuotas + 1):
        pagos.append({
            "Cuota": i,
            "Fecha": fecha_actual.strftime('%d/%m/%Y'),
            "Monto": f"${round(monto_cuota, 2):,}"
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

    # Sidebar: Registro de datos
    with st.sidebar:
        st.header("➕ Nuevo Registro")
        with st.form("registro_form", clear_on_submit=True):
            cliente = st.text_input("Nombre del Cliente")
            monto = st.number_input("Monto Total", min_value=0.0, step=1000.0)
            cuotas = st.number_input("Cantidad de Cuotas", min_value=1, step=1)
            frecuencia = st.selectbox("Frecuencia de Cobro", ["Diario", "Semanal", "Mensual"])
            fecha = st.date_input("Fecha del Préstamo", datetime.now())
            
            if st.form_submit_button("Guardar en Agenda"):
                if cliente:
                    plan = calcular_calendario(monto, cuotas, fecha, frecuencia)
                    st.session_state.db.append({
                        "id": len(st.session_state.db),
                        "cliente": cliente, 
                        "plan": plan, 
                        "monto": monto,
                        "notas": "" # Espacio para escribir datos extra
                    })
                    st.rerun()

    # Panel Principal: Visualización y Escritura
    if st.session_state.db:
        # Buscador rápido
        busqueda = st.text_input("🔍 Buscar cliente por nombre...")
        
        for idx, item in enumerate(st.session_state.db):
            if busqueda.lower() in item['cliente'].lower():
                with st.expander(f"👤 CLIENTE: {item['cliente']} | Total: ${item['monto']:,}"):
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.subheader("📅 Cronograma de Pagos")
                        st.table(pd.DataFrame(item['plan']))
                    
                    with col2:
                        st.subheader("📝 Notas y Datos")
                        # Aquí Martin puede escribir datos directamente
                        nota_key = f"nota_{idx}"
                        st.session_state.db[idx]['notas'] = st.text_area(
                            "Escribe observaciones (ej: Dirección, teléfono, aval):",
                            value=item['notas'],
                            key=nota_key
                        )
                        if st.button("Guardar Nota", key=f"btn_{idx}"):
                            st.success("Información actualizada.")

        # Botón para borrar todo si es necesario
        if st.sidebar.button("🗑️ Limpiar Agenda"):
            st.session_state.db = []
            st.rerun()
    else:
        st.info("No hay registros. Usa el panel de la izquierda para empezar.")

if __name__ == "__main__":
    main()
