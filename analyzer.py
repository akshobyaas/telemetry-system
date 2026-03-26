import pandas as pd
from sklearn.ensemble import IsolationForest

FILE_NAME = "data_log.csv"
WINDOW_SIZE = 30

# Train ML model once
model = None

def train_model(df):
    global model
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(df[["cpu", "memory"]])


def get_recent_data():
    try:
        df = pd.read_csv(FILE_NAME)
        return df.tail(WINDOW_SIZE)
    except:
        return pd.DataFrame()


def detect_trend(df):
    # 🔴 FIX: handle empty or small data
    if df.empty or len(df) < 2:
        return None

    memory_values = df["memory"].values
    cpu_values = df["cpu"].values

    # Memory leak detection (improved)
    if sum(y > x for x, y in zip(memory_values, memory_values[1:])) > len(memory_values) * 0.7:
        return "Memory Leak Suspected"

    # CPU instability detection
    if (max(cpu_values) - min(cpu_values)) > 50:
        return "CPU Instability Detected"

    return None


def detect_statistical(df, data):
    avg_cpu = df["cpu"].mean()
    avg_memory = df["memory"].mean()

    cpu = data["cpu"]
    memory = data["memory"]

    if (
        cpu > avg_cpu + 20 or cpu < avg_cpu - 20 or
        memory > avg_memory + 20 or memory < avg_memory - 20
    ):
        return True

    return False


def detect_ml(data):
    global model
    if model is None:
        return False

    input_df = pd.DataFrame([[data["cpu"], data["memory"]]], columns=["cpu", "memory"])
    prediction = model.predict(input_df)

    return prediction[0] == -1

def analyze(data):
    
    # Thermal check
    thermal_issue = detect_thermal_issue(data)
    if thermal_issue:
        return thermal_issue

    power_issue = detect_power_issue(data)
    if power_issue:
        return power_issue

    df = get_recent_data()

    # Train ML if enough data
    if len(df) > 20:
        train_model(df)

    # 1. Trend detection (highest priority)
    trend = detect_trend(df)
    if trend:
        return trend

    # 2. Statistical anomaly
    stat_flag = detect_statistical(df, data)

    # 3. ML anomaly
    ml_flag = detect_ml(data)

    # 4. Decision logic
    if stat_flag and ml_flag:
        return "Confirmed Anomaly"

    if stat_flag or ml_flag:
        return "Suspicious"

    return "Normal"

def detect_thermal_issue(data):
    if data["temperature"] > 75 and data["cpu"] < 50:
        return "Abnormal Thermal Rise"
    return None


def detect_power_issue(data):
    if data["power"] > 200 and data["cpu"] < 50:
        return "Power Spike Detected"
    return None