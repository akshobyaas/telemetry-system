import psutil, random
from datetime import datetime

def get_data():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent

    # Simulated temperature (based on CPU)
    temperature = 40 + (cpu * 0.3) + random.uniform(-2, 2)

    # Simulated power usage (based on CPU)
    power = 100 + (cpu * 1.5) + random.uniform(-5, 5)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "time": timestamp,
        "cpu": cpu,
        "memory": memory,
        "temperature": round(temperature, 2),
        "power": round(power, 2)
    }