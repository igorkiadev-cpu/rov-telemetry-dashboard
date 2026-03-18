import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="ROV Mission Intelligence", layout="wide")

# ======================
# HEADER
# ======================
st.title("ROV Mission Intelligence Platform")
st.caption("Real-time telemetry analysis tool for offshore ROV operations")

st.markdown("""
Analyze ROV telemetry data to extract operational insights,
monitor depth profiles, and improve subsea mission performance.
""")

st.info("Upload your mission data or use the sample dataset.")

# ======================
# DATA LOADING
# ======================
uploaded_file = st.file_uploader("Upload ROV Telemetry CSV", type=["csv"])

# Caminho padrão (tenta encontrar o CSV em raiz ou na pasta data/)
default_csv_paths = ["rov_mission_data.csv", "data/rov_mission_data.csv"]

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    # procura o CSV padrão
    csv_found = False
    for path in default_csv_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            csv_found = True
            break
    if not csv_found:
        st.error("❌ CSV padrão não encontrado! Faça upload do arquivo.")
        st.stop()

# ======================
# FILTER
# ======================
time_range = st.slider(
    "Select mission time range",
    int(df["time"].min()),
    int(df["time"].max()),
    (int(df["time"].min()), int(df["time"].max()))
)

filtered_df = df[
    (df["time"] >= time_range[0]) &
    (df["time"] <= time_range[1])
]

# ======================
# KPIs
# ======================
st.subheader("Mission Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Max Depth (m)", f"{filtered_df['depth'].max():.1f}")
col2.metric("Min Altitude (m)", f"{filtered_df['altitude'].min():.1f}")
col3.metric("Max Temperature (°C)", f"{filtered_df['temperature'].max():.1f}")

# ======================
# ALERT
# ======================
if filtered_df["depth"].max() > 100:
    st.warning("⚠️ Depth exceeded safe operational threshold!")

# ======================
# INSIGHTS
# ======================
st.subheader("Operational Insights")
st.write(f"""
- Maximum depth reached: {filtered_df['depth'].max():.1f} m  
- Average altitude: {filtered_df['altitude'].mean():.1f} m  
- Temperature peak: {filtered_df['temperature'].max():.1f} °C  
""")

# ======================
# DATA TABLE
# ======================
st.subheader("Mission Data Explorer")
st.dataframe(filtered_df)

# ======================
# CHARTS
# ======================
st.subheader("Data Visualization")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Depth Analysis")
    fig1 = px.line(filtered_df, x="time", y="depth")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### Depth vs Altitude")
    fig2 = px.line(filtered_df, x="time", y=["depth", "altitude"])
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("### Thermal Monitoring")
fig3 = px.line(filtered_df, x="time", y="temperature")
st.plotly_chart(fig3, use_container_width=True)

# ======================
# DOWNLOAD
# ======================
st.download_button(
    "Download Filtered Data",
    filtered_df.to_csv(index=False),
    file_name="filtered_rov_data.csv"
)
