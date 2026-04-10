import numpy as np

def increasing_trend(values, threshold=0.7):
    increases = sum(y > x for x, y in zip(values, values[1:]))
    return increases > len(values) * threshold


def high_variation(values, threshold=50):
    return (max(values) - min(values)) > threshold


def get_root_cause(df, latest_data):
    causes = []
    confidence = 0.0

    if df.empty or len(df) < 5:
        return {
            "cause": "Insufficient Data",
            "details": "Not enough data for diagnosis",
            "confidence": 0.0
        }

    cpu = df["cpu"].values
    memory = df["memory"].values
    temp = df["temperature"].values
    power = df["power"].values

    # 🔴 Memory Leak
    if increasing_trend(memory):
        causes.append(("Memory Leak", 0.8))

    # 🔴 CPU Instability
    if high_variation(cpu):
        causes.append(("CPU Instability", 0.75))

    # 🔴 Overheating
    if latest_data["temperature"] > 80 and latest_data["cpu"] < 50:
        causes.append(("Overheating", 0.9))

    # 🔴 Power Spike
    if latest_data["power"] > 220 and latest_data["cpu"] < 50:
        causes.append(("Power Spike", 0.85))

    # 🔴 System Overload
    if latest_data["cpu"] > 85 and latest_data["memory"] > 85:
        causes.append(("System Overload", 0.9))

    if not causes:
        return {
            "cause": "Unknown",
            "details": "No clear failure pattern detected",
            "confidence": 0.3
        }

    # pick highest confidence cause
    best_cause = max(causes, key=lambda x: x[1])

    return {
        "cause": best_cause[0],
        "details": f"Detected pattern: {best_cause[0]}",
        "confidence": best_cause[1]
    }