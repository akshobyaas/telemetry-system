import psutil
import random
from datetime import datetime
import requests


# 🔥 Get real temperature and power using LibreHardwareMonitor Web API
def get_real_temp_power():
    try:
        url = "http://localhost:8085/data.json"
        response = requests.get(url, timeout=2)
        data = response.json()

        temperature = None
        power = None

        def extract(node):
            nonlocal temperature, power

            if isinstance(node, dict):
                text = node.get("Text", "")
                value = node.get("Value", "")

                # 🌡️ Temperature
                if "CPU Package" in text and "°C" in value:
                    temperature = float(value.replace(" °C", ""))

                # ⚡ Power
                if "CPU Package" in text and "W" in value:
                    power = float(value.replace(" W", ""))

                # Recurse into children
                for child in node.get("Children", []):
                    extract(child)

        extract(data)

        return temperature, power

    except Exception as e:
        # print("Sensor Error:", e)  # optional debug
        return None, None


def get_data():
    cpu = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory().percent

    temperature, power = get_real_temp_power()

    temp_source = "real"
    power_source = "real"

    # 🔁 Fallback (if sensor fails)
    if  temperature is None:
        temperature = 40 + (cpu * 0.3) + random.uniform(-2, 2)
        temp_source = "fallback"

    if power is None:
        power = 80 + (cpu * 1.5) + random.uniform(-5, 5)
        power_source = "fallback"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
    "time": timestamp,
    "cpu": cpu,
    "memory": memory,
    "temperature": round(temperature, 2),
    "power": round(power, 2),
    "temp_source": temp_source,
    "power_source": power_source
}