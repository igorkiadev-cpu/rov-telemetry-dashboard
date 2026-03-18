import streamlit as st

st.set_page_config(page_title="ROV Mission Intelligence", layout="wide")

st.title("ROV Mission Intelligence Dashboard")

st.markdown("""
Analyze ROV telemetry data to extract operational insights, monitor depth profiles,
and improve subsea mission performance.
""")

st.info("Upload your mission data or use the sample dataset to explore insights.")

import streamlit as st
import pandas as pd

st.title("ROV Telemetry Dashboard")

uploaded_file = st.file_uploader("Upload ROV Telemetry CSV", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    data = pd.read_csv("data/rov_mission_data.csv")

max_time = st.slider(
    "Select mission time",
    0,
    int(data["time"].max()),
    int(data["time"].max())
)

filtered_data = data[data["time"] <= max_time]

st.subheader("Telemetry Data")
st.dataframe(filtered_data)

st.subheader("Mission Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Max Depth", filtered_data["depth"].max())
col2.metric("Min Altitude", filtered_data["altitude"].min())
col3.metric("Max Temperature", filtered_data["temperature"].max())

st.subheader("Depth Profile")
st.line_chart(filtered_data["depth"])

st.subheader("Depth vs Altitude")
st.line_chart(filtered_data[["depth","altitude"]])

st.subheader("Temperature Variation")
st.line_chart(filtered_data["temperature"])
