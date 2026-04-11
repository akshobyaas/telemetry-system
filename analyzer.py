import pandas as pd
from ml_model import train_model, predict
from root_cause import get_root_cause

FILE_NAME = "data_log.csv"

model_trained = False


def detect_trend(df):
    if len(df) < 5:
        return None

    if df["cpu"].iloc[-1] > df["cpu"].iloc[-5]:
        return "Increasing CPU Trend"

    if df["memory"].iloc[-1] > df["memory"].iloc[-5]:
        return "Increasing Memory Trend"

    return None


def analyze(data):
    global model_trained

    try:
        df = pd.read_csv(FILE_NAME)
    except:
        df = pd.DataFrame()

    # Train model once enough data
    if not model_trained and len(df) > 30:
        train_model(df)
        model_trained = True

    is_anomaly, prob = predict(data, df) if model_trained else (False, 0.0)

    trend = detect_trend(df)

    root = get_root_cause(df, data)

    # 🔥 FINAL DECISION LOGIC
    if is_anomaly:
        status = "Confirmed Anomaly"
    elif trend:
        status = "Suspicious"
    else:
        status = "Normal"

    return {
        "status": status,
        "cause": root.get("cause") if status != "Normal" else "None",
        "confidence": round(prob if prob else root.get("confidence", 0), 2)
    }