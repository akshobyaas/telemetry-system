import subprocess
import sys
import time

print("Starting system...")

# start main.py
main_process = subprocess.Popen([sys.executable, "main.py"])

# small delay
time.sleep(2)

# start dashboard
dashboard_process = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", "dashboard.py"]
)

print("Running... Press Ctrl+C to stop")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping...")

    main_process.terminate()
    dashboard_process.terminate()

    print("Stopped.")