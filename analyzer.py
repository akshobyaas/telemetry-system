import pandas as pd
from ml_model import train_model, predict
from root_cause import get_root_cause

FILE_NAME = "data_log.csv"
WINDOW_SIZE = 30


def get_recent_data():
    try:
        df = pd.read_csv(FILE_NAME)
        return df.tail(WINDOW_SIZE)
    except:
        return pd.DataFrame()


# ==============================
# 🔍 TREND DETECTION
# ==============================
def detect_trend(df):
    if df.empty or len(df) < 2:
        return None

    memory_values = df["memory"].values
    cpu_values = df["cpu"].values

    # Memory leak
    if sum(y > x for x, y in zip(memory_values, memory_values[1:])) > len(memory_values) * 0.7:
        return "Memory Leak Suspected"

    # CPU instability
    if (max(cpu_values) - min(cpu_values)) > 50:
        return "CPU Instability Detected"

    return None


# ==============================
# 📊 STATISTICAL DETECTION
# ==============================
def detect_statistical(df, data):
    if df.empty:
        return False

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


# ==============================
# 🔥 SPECIAL RULES
# ==============================
def detect_thermal_issue(data):
    if data["temperature"] > 75 and data["cpu"] < 50:
        return "Abnormal Thermal Rise"
    return None


def detect_power_issue(data):
    if data["power"] > 200 and data["cpu"] < 50:
        return "Power Spike Detected"
    return None

# ==============================
# 🚨 EXTREME CONDITIONS
# ==============================
def detect_extreme(data):
    if data["cpu"] > 95:
        return "CPU Saturation"

    if data["memory"] > 95:
        return "Memory Saturation"

    return None


# ==============================
# 🔁 SUSTAINED OVERLOAD
# ==============================
def detect_stuck_high(df):
    if df.empty or len(df) < 10:
        return None

    recent_cpu = df["cpu"].tail(10)

    if all(v > 95 for v in recent_cpu):
        return "CPU Stuck at 100%"

    return None
# ==============================
# 🧠 MAIN ANALYSIS ENGINE
# ==============================
def analyze(data):
    df = get_recent_data()
    
    # 🚨 Priority 0: Extreme conditions
    extreme = detect_extreme(data)
    if extreme:
        return {
            "status": extreme,
            "cause": "Resource Saturation",
            "details": "System running at extreme capacity",
            "confidence": 0.95
        }
    
    # 🔁 Priority 0.5: Sustained overload
    stuck = detect_stuck_high(df)
    if stuck:
        return {
            "status": stuck,
            "cause": "Sustained Overload",
            "details": "CPU continuously maxed out",
            "confidence": 0.9
       }

    # 🔥 Priority 1: Direct hardware issues
    thermal_issue = detect_thermal_issue(data)
    if thermal_issue:
        return {
            "status": thermal_issue,
            "cause": "Overheating",
            "details": "High temperature with low CPU usage",
            "confidence": 0.9
        }

    power_issue = detect_power_issue(data)
    if power_issue:
        return {
            "status": power_issue,
            "cause": "Power Spike",
            "details": "High power consumption with low CPU usage",
            "confidence": 0.9
        }

    # Train ML
    if len(df) > 30:
        train_model(df)

    # 🔍 Trend detection
    trend = detect_trend(df)

    # 📊 Statistical anomaly
    stat_flag = detect_statistical(df, data)

    # 🤖 ML prediction
    ml_flag, ml_conf = predict(data, df)
    
    

    # ==============================
    # 🧠 DECISION LOGIC
    # ==============================

    # 🔥 Strong anomaly
    if stat_flag and ml_flag:
        root = get_root_cause(df, data)
        return {
            "status": "Confirmed Anomaly",
            "ml_confidence": round(ml_conf, 2),
            **root
        }

    # 🔮 Prediction BEFORE failure
    if ml_flag:
        root = get_root_cause(df, data)
        return {
            "status": "Predicted Failure",
            "ml_confidence": round(ml_conf, 2),
            **root
        }

    # ⚠️ Weak anomaly
    if stat_flag:
        root = get_root_cause(df, data)
        return {
            "status": "Suspicious",
            "ml_confidence": round(ml_conf, 2),
            **root
        }

    # 📉 Trend-based warning
    if trend:
        return {
            "status": trend,
            "cause": trend,
            "details": "Trend-based anomaly detected",
            "confidence": 0.7
        }

    # ✅ Normal
    return {
        "status": "Normal",
        "cause": None,
        "details": None,
        "confidence": 1.0
    }