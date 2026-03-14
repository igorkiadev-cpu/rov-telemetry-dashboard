import streamlit as st
import pandas as pd

st.title("ROV Telemetry Dashboard")

st.write("Dashboard for analyzing ROV mission telemetry data.")

uploaded_file = st.file_uploader("Upload ROV Telemetry CSV", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    data = pd.read_csv("data/rov_mission_data.csv")

st.subheader("Telemetry Data")
st.dataframe(data)
