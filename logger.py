import csv
import os

FILE_NAME = "data_log.csv"

def create_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["time", "cpu", "memory", "temperature", "power", "temp_source", "power_source", "status", "cause", "confidence"])

def write_data(data, status):
    with open(FILE_NAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
    data["time"],
    data["cpu"],
    data["memory"],
    data["temperature"],
    data["power"],
    data["temp_source"],
    data["power_source"],
    status["status"],
    status.get("cause"),
    status.get("confidence")
])