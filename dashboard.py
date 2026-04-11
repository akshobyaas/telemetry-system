import streamlit as st
import pandas as pd
from pandas.errors import EmptyDataError
from offline_analyzer import analyze_csv
from analyzer import analyze
from datetime import datetime
import plotly.graph_objects as go   # ✅ FIX + UPGRADE

FILE_NAME = "data_log.csv"

ERROR_STATUSES = {
    "Confirmed Anomaly",
    "Memory Leak Suspected",
    "CPU Instability Detected",
    "Abnormal Thermal Rise",
    "Power Spike Detected",
}

st.set_page_config(page_title="Telemetry Dashboard", layout="wide")

st.title("🚀 Server Telemetry Dashboard")

# =========================
# SIDEBAR
# =========================
st.sidebar.title("Controls")

time_option = st.sidebar.selectbox(
    "Time Range",
    ["Last 10", "Last 30", "Last 100", "Full"]
)

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

# =========================
# 🧪 MANUAL TEST
# =========================
st.sidebar.markdown("---")
st.sidebar.subheader("Manual Test")

manual_cpu = st.sidebar.text_input("CPU (%)", placeholder="Enter value (0–100)")
manual_memory = st.sidebar.text_input("Memory (%)", placeholder="Enter value (0–100)")
manual_temp = st.sidebar.text_input("Temperature (°C)", placeholder="Enter value (20–100)")
manual_power = st.sidebar.text_input("Power (W)", placeholder="Enter value (50–800)")

run_test = st.sidebar.button("Run Test")


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

    # Time filter
    if time_option == "Last 10":
        df = df.tail(10)
    elif time_option == "Last 30":
        df = df.tail(30)
    elif time_option == "Last 100":
        df = df.tail(100)

    latest = df.iloc[-1]

    # =========================
    # TOP METRICS
    # =========================
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("CPU (%)", round(latest["cpu"], 1))
    c2.metric("Memory (%)", round(latest["memory"], 1))
    c3.metric("Temp (°C)", round(latest["temperature"], 1))
    c4.metric("Power (W)", round(latest["power"], 1))

    st.caption(f"Last updated: {latest['time']}")

    # Status banner
    if latest["status"] in ERROR_STATUSES:
        st.error(f"🚨 {latest['status']}")
    elif latest["status"] == "Suspicious":
        st.warning(f"⚠️ {latest['status']}")
    else:
        st.success("✅ System Normal")

    # =========================
    # 🔥 COMBO GRAPH (UPGRADED)
    # =========================
    st.subheader("📊 Performance Overview")

    x = pd.to_datetime(df["time"])
    fig = go.Figure()

    # Line trends
    fig.add_trace(go.Scatter(x=x, y=df["cpu"], mode='lines', name='CPU (%)', line=dict(width=3)))
    fig.add_trace(go.Scatter(x=x, y=df["memory"], mode='lines', name='Memory (%)', line=dict(width=3, dash='dot')))
    fig.add_trace(go.Scatter(x=x, y=df["temperature"], mode='lines', name='Temperature', yaxis='y2'))
    fig.add_trace(go.Scatter(x=x, y=df["power"], mode='lines', name='Power', yaxis='y2', line=dict(dash='dot')))

    # 🔴 Highlight anomalies
    anomalies = df[df["status"].isin(ERROR_STATUSES)]

    fig.add_trace(go.Scatter(
        x=pd.to_datetime(anomalies["time"]),
        y=anomalies["cpu"],
        mode='markers',
        name='Anomalies',
        marker=dict(size=10, color='red', symbol='x')
    ))

    fig.update_layout(
        height=500,
        xaxis_title="Time",
        yaxis=dict(title="CPU / Memory (%)"),
        yaxis2=dict(title="Temp / Power", overlaying='y', side='right'),
        hovermode="x unified",
        template="plotly_dark",
        legend=dict(orientation="h")
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # 🔍 SCATTER RELATION
    # =========================
    st.subheader("🔍 CPU vs Memory Analysis")

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=df["cpu"],
        y=df["memory"],
        mode='markers',
        marker=dict(size=8),
        name="System Behavior"
    ))

    fig2.update_layout(
        xaxis_title="CPU (%)",
        yaxis_title="Memory (%)",
        template="plotly_dark"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # =========================
    # 🧠 DIAGNOSIS
    # =========================
    st.subheader("🧠 Diagnosis")

    st.markdown(f"""
    **Status:** {latest['status']}  
    **Cause:** {latest.get('cause', 'N/A')}  
    **Confidence:** {latest.get('confidence') if latest.get('confidence') else latest.get('ml_confidence', 'N/A')}
    """)

    # =========================
    # 📋 LOGS
    # =========================
    st.subheader("📋 Recent Logs")
    st.dataframe(df.tail(10), use_container_width=True)


# Run dashboard
render_dashboard()


# =========================
# 🧪 MANUAL TEST RESULT
# =========================
if run_test:

    # ✅ Step 1: Check empty
    if manual_cpu == "" or manual_memory == "" or manual_temp == "" or manual_power == "":
        st.warning("⚠️ Please fill all fields")
        st.stop()

    # ✅ Step 2: Convert to float
    try:
        manual_cpu = float(manual_cpu)
        manual_memory = float(manual_memory)
        manual_temp = float(manual_temp)
        manual_power = float(manual_power)
    except:
        st.error("❌ Please enter valid numeric values")
        st.stop()

    # ✅ Step 3: Range validation (NOW SAFE)
    if not (0 <= manual_cpu <= 100):
        st.error("CPU must be between 0–100")
        st.stop()

    if not (0 <= manual_memory <= 100):
        st.error("Memory must be between 0–100")
        st.stop()

    if not (20 <= manual_temp <= 100):
        st.error("Temperature must be between 20–100 °C")
        st.stop()

    if not (50 <= manual_power <= 800):
        st.error("Power must be between 50–800 W")
        st.stop()

    # ✅ Step 4: Prepare data
    test_data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu": manual_cpu,
        "memory": manual_memory,
        "temperature": manual_temp,
        "power": manual_power,
        "temp_source": "manual",
        "power_source": "manual"
    }

    # ✅ Step 5: Analyze
    result = analyze(test_data)

    # ✅ Step 6: Display
    st.markdown("---")
    st.subheader("🧪 Manual Test Result")

    if result["status"] in ERROR_STATUSES:
        st.error(result["status"])
    elif result["status"] == "Suspicious":
        st.warning(result["status"])
    else:
        st.success(result["status"])

    st.write("Cause:", result.get("cause"))
    st.write("Confidence:", result.get("confidence", result.get("ml_confidence")))

# =========================
# 📂 CSV UPLOAD ANALYSIS
# =========================
if uploaded_file is not None:
    st.subheader("📂 Uploaded Data Analysis")

    try:
        df_uploaded = pd.read_csv(uploaded_file)
        uploaded_file.seek(0)

        result = analyze_csv(uploaded_file)

        if "error" in result:
            st.error(result["error"])
        else:
            st.write("### Summary")
            for item in result["summary"]:
                st.write("-", item)

            st.write("### Root Cause")
            st.write(result["root_cause"])

    except Exception as e:
        st.error(e)