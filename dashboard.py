import streamlit as st
import pandas as pd
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

    # 📊 Latest Data
    st.subheader("Latest Data")
    st.dataframe(df.tail(10), use_container_width=True)

    # 📈 Charts
    st.subheader("CPU Usage")
    st.line_chart(df["cpu"])

    st.subheader("Memory Usage")
    st.line_chart(df["memory"])

    st.subheader("Temperature")
    st.line_chart(df["temperature"])

    st.subheader("Power Consumption")
    st.line_chart(df["power"])

    # 📊 Status Summary
    st.subheader("Status Summary")
    st.write(df["status"].value_counts())

    # 🚨 Latest Status
    latest_status = df.iloc[-1]["status"]

    st.subheader("Latest System Status")
    if latest_status in ERROR_STATUSES:
        st.error(latest_status)
    elif latest_status == "Suspicious":
        st.warning(latest_status)
    else:
        st.success(latest_status)

    # 🧠 Root Cause Table (safe check)
    st.subheader("Root Cause")
    if "cause" in df.columns:
        st.write(df[["time", "status", "cause"]].tail(10))
    else:
        st.info("Root cause data not available yet.")

    # 🔍 Latest Diagnosis
    latest = df.iloc[-1]

    st.subheader("Latest Diagnosis")
    st.write(f"Status: {latest['status']}")
    st.write(f"Cause: {latest.get('cause', 'N/A')}")
    st.write(f"Confidence: {latest.get('confidence', 'N/A')}")


# ▶️ Run live dashboard
render_dashboard()


# ==============================
# 📂 CSV UPLOAD ANALYSIS FEATURE
# ==============================

st.divider()

st.sidebar.header("Upload Dataset for Analysis")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    st.subheader("📂 Uploaded Dataset Analysis")

    try:
        df_uploaded = pd.read_csv(uploaded_file)
        
        uploaded_file.seek(0)  # Reset file pointer for analysis

        result = analyze_csv(uploaded_file)

        if "error" in result:
            st.error(result["error"])
        else:
            # 🧠 Summary
            st.subheader("Summary")
            for item in result["summary"]:
                st.write(f"- {item}")

            # 🔍 Root Cause
            st.subheader("Root Cause")
            st.write(f"Cause: {result['root_cause']['cause']}")
            st.write(f"Details: {result['root_cause']['details']}")
            st.write(f"Confidence: {result['root_cause']['confidence']}")

            # 📊 Statistics
            st.subheader("Statistics")
            st.json(result["stats"])

            # 📈 Charts
            st.subheader("Uploaded Data Visualization")
            st.line_chart(df_uploaded[["cpu", "memory"]])
            st.line_chart(df_uploaded[["temperature", "power"]])
            
            st.subheader("Sensor Data Source")

            if "temp_source" in df_uploaded.columns and "power_source" in df_uploaded.columns:
                st.write(df_uploaded[["time", "temp_source", "power_source"]].tail(10))

    except Exception as e:
        st.error(f"Error processing file: {e}")