import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pandas.errors import EmptyDataError
from offline_analyzer import analyze_csv

FILE_NAME = "data_log.csv"

ERROR_STATUSES = {
    "Confirmed Anomaly",
    "Memory Leak Suspected",
    "CPU Instability Detected",
    "Abnormal Thermal Rise",
    "Power Spike Detected",
}

st.set_page_config(page_title="Telemetry Dashboard", layout="wide")

st.title("Server Telemetry Dashboard")

# Sidebar
st.sidebar.title("Controls")
time_option = st.sidebar.selectbox(
    "Time Range",
    ["Last 10", "Last 30", "Last 100", "Full"]
)

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])


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

    # Apply filter
    if time_option == "Last 10":
        df = df.tail(10)
    elif time_option == "Last 30":
        df = df.tail(30)
    elif time_option == "Last 100":
        df = df.tail(100)

    latest = df.iloc[-1]

    # -----------------------------
    # Top metrics
    # -----------------------------
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("CPU (%)", round(latest["cpu"], 1))
    c2.metric("Memory (%)", round(latest["memory"], 1))
    c3.metric("Temp (°C)", round(latest["temperature"], 1))
    c4.metric("Power (W)", round(latest["power"], 1))

    # Status banner
    if latest["status"] in ERROR_STATUSES:
        st.error(f"Status: {latest['status']}")
    elif latest["status"] == "Suspicious":
        st.warning(f"Status: {latest['status']}")
    else:
        st.success("Status: Normal")

    # -----------------------------
    # Charts
    # -----------------------------
    st.subheader("Performance")

    x = pd.to_datetime(df["time"])

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        ax.plot(x, df["cpu"], label="CPU")
        ax.plot(x, df["memory"], label="Memory")
        ax.set_xlabel("Time")
        ax.set_ylabel("Usage (%)")
        ax.set_title("CPU & Memory")
        ax.legend()
        ax.grid(True)
        plt.xticks(rotation=30)
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        ax.plot(x, df["temperature"], label="Temperature")
        ax.plot(x, df["power"], label="Power")
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.set_title("Temperature & Power")
        ax.legend()
        ax.grid(True)
        plt.xticks(rotation=30)
        st.pyplot(fig)

    # -----------------------------
    # Diagnosis
    # -----------------------------
    st.subheader("Diagnosis")

    st.write("Status:", latest["status"])
    st.write("Cause:", latest.get("cause", "N/A"))
    st.write("Confidence:", latest.get("confidence", "N/A"))

    # -----------------------------
    # Logs
    # -----------------------------
    st.subheader("Recent Logs")
    st.dataframe(df.tail(10), width="stretch")


render_dashboard()

# -----------------------------
# Upload Analysis
# -----------------------------
if uploaded_file is not None:
    st.subheader("Uploaded Data Analysis")

    try:
        df_uploaded = pd.read_csv(uploaded_file)
        uploaded_file.seek(0)

        result = analyze_csv(uploaded_file)

        if "error" in result:
            st.error(result["error"])
        else:
            st.write("Summary:")
            for item in result["summary"]:
                st.write("-", item)

            st.write("Root Cause:")
            st.write(result["root_cause"])

            fig, ax = plt.subplots()
            ax.plot(df_uploaded["cpu"], label="CPU")
            ax.plot(df_uploaded["memory"], label="Memory")
            ax.legend()
            ax.set_title("CPU vs Memory")
            st.pyplot(fig)

    except Exception as e:
        st.error(e)