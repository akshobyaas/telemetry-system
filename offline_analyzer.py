import pandas as pd
from root_cause import get_root_cause
from analyzer import detect_trend


def analyze_csv(file_path):
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return {"error": f"Failed to read file: {e}"}

    if df.empty or len(df) < 5:
        return {"error": "Not enough data for analysis"}

    latest_data = df.iloc[-1].to_dict()

    # 🔍 Trend detection
    trend = detect_trend(df)

    # 🧠 Root cause detection
    root = get_root_cause(df, latest_data)

    # 📊 Stats
    stats = {
        "max_cpu": df["cpu"].max(),
        "avg_cpu": df["cpu"].mean(),
        "max_memory": df["memory"].max(),
        "avg_memory": df["memory"].mean(),
        "max_temp": df["temperature"].max(),
        "max_power": df["power"].max(),
    }

    # 🧾 Build summary
    summary = []

    if trend:
        summary.append(trend)

    if root["cause"]:
        summary.append(root["cause"])

    return {
        "status": "Analysis Complete",
        "summary": summary,
        "root_cause": root,
        "stats": stats
    }
    
    
def print_report(result):
    if "error" in result:
        print(result["error"])
        return

    print("\n===== SYSTEM ANALYSIS REPORT =====\n")

    print("Status:", result["status"])

    print("\nDetected Issues:")
    for item in result["summary"]:
        print("-", item)

    print("\nRoot Cause:")
    print("Cause:", result["root_cause"]["cause"])
    print("Details:", result["root_cause"]["details"])
    print("Confidence:", result["root_cause"]["confidence"])

    print("\nStatistics:")
    for k, v in result["stats"].items():
        print(f"{k}: {round(v, 2)}")