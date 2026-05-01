import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configuración de página
st.set_page_config(page_title="Gestión de Préstamos Pro", layout="wide")

def calcular_calendario(monto, cuotas, fecha_inicio, frecuencia):
    pagos = []
    monto_cuota = monto / cuotas
    fecha_actual = fecha_inicio
    
    for i in range(1, cuotas + 1):
        pagos.append({
            "N° Cuota": i,
            "Fecha de Pago": fecha_actual,
            "Monto": round(monto_cuota, 2),
            "Estado": "Pendiente"
        })
        if frecuencia == "Diario":
            fecha_actual += timedelta(days=1)
        elif frecuencia == "Semanal":
            fecha_actual += timedelta(weeks=1)
        else: # Mensual
            fecha_actual += timedelta(days=30)
    return pagos

def main():
    st.title("🏦 Sistema de Gestión de Préstamos - Dashboard")
    st.markdown("---")

    # Inicializar estado de la sesión para 10 clientes
    if 'clientes' not in st.session_state:
        st.session_state.clientes = []

    # Sidebar para entrada de datos
    with st.sidebar:
        st.header("Registro de Nuevo Préstamo")
        with st.form("form_prestamo"):
            nombre = st.text_input("Nombre del Cliente")
            monto = st.number_input("Monto del Préstamo", min_value=0.0, step=100.0)
            cuotas = st.number_input("Cantidad de Cuotas", min_value=1, max_value=360, step=1)
            fecha_prestamo = st.date_input("Fecha del Préstamo", datetime.now())
            frecuencia = st.selectbox("Frecuencia de Pago", ["Diario", "Semanal", "Mensual"])
            
            submit = st.form_submit_button("Registrar Cliente")
            
            if submit and nombre:
                if len(st.session_state.clientes) < 10:
                    plan_pagos = calcular_calendario(monto, cuotas, fecha_prestamo, frecuencia)
                    st.session_state.clientes.append({
                        "Cliente": nombre,
                        "Monto Total": monto,
                        "Cuotas": cuotas,
                        "Frecuencia": frecuencia,
                        "Calendario": plan_pagos
                    })
                    st.success(f"Cliente {nombre} registrado.")
                else:
                    st.error("Límite de 10 clientes alcanzado para esta demo.")

    # Visualización Principal
    if st.session_state.clientes:
        # Resumen General
        st.subheader("📋 Resumen de Cartera")
        df_resumen = pd.DataFrame(st.session_state.clientes).drop(columns=['Calendario'])
        st.table(df_resumen)

        st.markdown("---")
        
        # Detalle por Cliente (Agenda)
        st.subheader("📅 Agenda de Cobros Detallada")
        
        for idx, c in enumerate(st.session_state.clientes):
            with st.expander(f"Ver Cronograma: {c['Cliente']}"):
                df_pagos = pd.DataFrame(c['Calendario'])
                # Formatear fecha para visualización
                df_pagos['Fecha de Pago'] = df_pagos['Fecha de Pago'].dt.strftime('%Y-%m-%d')
                st.dataframe(df_pagos, use_container_width=True)
                
    else:
        st.info("No hay clientes registrados. Use el panel lateral para agregar datos.")

if __name__ == "__main__":
    main()
