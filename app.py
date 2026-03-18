import streamlit as st
import pandas as pd
import plotly.express as px

# Config
st.set_page_config(page_title="ROV Mission Intelligence", layout="wide")

# Header
st.title("ROV Mission Intelligence Dashboard")

st.markdown("""
Analyze ROV telemetry data to extract operational insights,
monitor depth profiles, and improve subsea mission performance.
""")

st.info("Upload your mission data or use the sample dataset.")

# Upload
uploaded_file = st.file_uploader("Upload ROV Telemetry CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("rov_mission_data.csv")

# Slider
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

# KPIs
st.subheader("Mission Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Max Depth (m)", f"{filtered_df['depth'].max():.1f}")
col2.metric("Min Altitude (m)", f"{filtered_df['altitude'].min():.1f}")
col3.metric("Max Temperature (°C)", f"{filtered_df['temperature'].max():.1f}")

# Data table
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# Charts
st.subheader("Depth Profile")
fig1 = px.line(filtered_df, x="time", y="depth")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Depth vs Altitude")
fig2 = px.line(filtered_df, x="time", y=["depth", "altitude"])
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Temperature Variation")
fig3 = px.line(filtered_df, x="time", y="temperature")
st.plotly_chart(fig3, use_container_width=True)

# Download
st.download_button(
    "Download Filtered Data",
    filtered_df.to_csv(index=False),
    file_name="filtered_rov_data.csv"
)
