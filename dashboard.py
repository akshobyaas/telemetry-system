import streamlit as st
import pandas as pd
from pandas.errors import EmptyDataError

FILE_NAME = "data_log.csv"
ERROR_STATUSES = {
    "Confirmed Anomaly",
    "Memory Leak Suspected",
    "CPU Instability Detected",
    "Abnormal Thermal Rise",
    "Power Spike Detected",
}

st.set_page_config(page_title="Telemetry Dashboard", layout="wide")

st.title("Server Telemetry Anomaly Detection")
st.caption("Auto-refreshing every 3 seconds")


@st.fragment(run_every="3s")
def render_dashboard():
    try:
        df = pd.read_csv(FILE_NAME)
    except (FileNotFoundError, EmptyDataError):
        st.info("Waiting for data...")
        return

    if df.empty:
        st.info("Waiting for data...")
        return

    st.subheader("Latest Data")
    st.dataframe(df.tail(10), use_container_width=True)

    st.subheader("CPU Usage")
    st.line_chart(df["cpu"])

    st.subheader("Memory Usage")
    st.line_chart(df["memory"])

    st.subheader("Temperature")
    st.line_chart(df["temperature"])

    st.subheader("Power Consumption")
    st.line_chart(df["power"])

    st.subheader("Status Summary")
    st.write(df["status"].value_counts())

    latest_status = df.iloc[-1]["status"]

    st.subheader("Latest System Status")
    if latest_status in ERROR_STATUSES:
        st.error(latest_status)
    elif latest_status == "Suspicious":
        st.warning(latest_status)
    else:
        st.success(latest_status)


render_dashboard()
