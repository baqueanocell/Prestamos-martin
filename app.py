import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configuración de página
st.set_page_config(page_title="Control de Préstamos Pro", layout="wide")

def calcular_calendario(monto, cuotas, fecha_inicio, frecuencia):
    pagos = []
    monto_cuota = monto / cuotas
    fecha_actual = fecha_inicio
    for i in range(1, cuotas + 1):
        pagos.append({
            "Cuota": i,
            "Fecha": fecha_actual.strftime('%Y-%m-%d'),
            "Monto": round(monto_cuota, 2)
        })
        if frecuencia == "Diario": fecha_actual += timedelta(days=1)
        elif frecuencia == "Semanal": fecha_actual += timedelta(weeks=1)
        else: fecha_actual += timedelta(days=30)
    return pagos

def main():
    st.title("🏦 Dashboard de Préstamos - Streaming Interface")
    
    if 'db' not in st.session_state:
        st.session_state.db = []

    # Panel de entrada
    with st.sidebar:
        st.header("⚙️ Configuración")
        with st.form("registro"):
            cliente = st.text_input("Nombre del Cliente")
            monto = st.number_input("Capital", min_value=0.0)
            cuotas = st.number_input("Cuotas", min_value=1)
            frecuencia = st.selectbox("Ciclo", ["Diario", "Semanal", "Mensual"])
            fecha = st.date_input("Fecha Inicio", datetime.now())
            if st.form_submit_button("Añadir a Agenda"):
                if cliente:
                    plan = calcular_calendario(monto, cuotas, fecha, frecuencia)
                    st.session_state.db.append({"cliente": cliente, "plan": plan, "monto": monto})

    # Display de Datos
    if st.session_state.db:
        cols = st.columns(len(st.session_state.db) if len(st.session_state.db) < 4 else 3)
        
        for idx, item in enumerate(st.session_state.db):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.subheader(f"👤 {item['cliente']}")
                    st.write(f"**Total:** ${item['monto']}")
                    df_aux = pd.DataFrame(item['plan'])
                    st.dataframe(df_aux, height=200, hide_index=True)

        # Botón de Respaldo (Backup CSV)
        st.divider()
        full_data = []
        for c in st.session_state.db:
            for p in c['plan']:
                full_data.append({"Cliente": c['cliente'], **p})
        
        df_export = pd.DataFrame(full_data)
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar Reporte Completo (CSV)", csv, "prestamos.csv", "text/csv")
    else:
        st.warning("Esperando ingreso de datos de clientes...")

if __name__ == "__main__":
    main()


