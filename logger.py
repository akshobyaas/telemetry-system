import csv
import os

FILE_NAME = "data_log.csv"

HEADERS = [
    "time", "cpu", "memory", "temperature", "power",
    "temp_source", "power_source",
    "status", "cause", "confidence"
]


def create_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)


def write_data(data, result):
    row = [
        data["time"],
        data["cpu"],
        data["memory"],
        data["temperature"],
        data["power"],
        data["temp_source"],
        data["power_source"],
        result["status"],
        result.get("cause"),
        result.get("confidence")
    ]

    with open(FILE_NAME, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)