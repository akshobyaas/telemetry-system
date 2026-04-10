import pandas as pd
from root_cause import get_root_cause
from analyzer import detect_trend   # ✅ safe now


def analyze_csv(file):
    try:
        df = pd.read_csv(file)
    except Exception as e:
        return {"error": f"Failed to read file: {e}"}

    if df.empty or len(df) < 5:
        return {"error": "Not enough data"}

    latest = df.iloc[-1].to_dict()

    trend = detect_trend(df)
    root = get_root_cause(df, latest)

    summary = []

    if trend:
        summary.append(trend)

    if root["cause"]:
        summary.append(root["cause"])

    return {
        "status": "Analysis Complete",
        "summary": summary,
        "root_cause": root
    }