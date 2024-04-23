import requests
import yaml
import sys
import os
import datetime
import subprocess


def get_ip():
    response = requests.get("https://api64.ipify.org?format=json").json()
    return response["ip"]


hwid = (
    subprocess.check_output("wmic csproduct get uuid").decode().split("\n")[1].strip()
)

try:
    if not os.path.exists("auth.yaml"):
        with open("auth.yaml", "w") as f:
            yaml.dump({"hwid": hwid, "key": ""}, f)

    with open("auth.yaml", "r") as f:
        data = yaml.safe_load(f)
        result = requests.get(
            f"http://localhost:8000/check_key/{hwid}/{data.get('key')}"
        )
        experiance_time = (datetime.datetime.now()).isoformat()
        if "experiance_time" in result.json():
            experiance_time_bd = result.json()["experiance_time"]
        else:
            pass
        if result.status_code == 200 and experiance_time_bd > experiance_time:
            print("Soft active")
            left_time = (
                datetime.datetime.fromisoformat(experiance_time_bd)
                - datetime.datetime.now()
            ).total_seconds()
            left_minutes, left_seconds = divmod(left_time, 60)
            left_hours, left_minutes = divmod(left_minutes, 60)
            left_days, left_hours = divmod(left_hours, 24)
            left_days = int(left_days)
            print(
                f"{left_days}:{int(left_hours):02d}:{int(left_minutes):02d}:{int(left_seconds):02d} осталось до {experiance_time_bd}"
            )
            sys.exit()
        elif experiance_time_bd < experiance_time:
            print("Key expired")
        else:
            print("Soft not active")
except FileNotFoundError:
    print("File 'auth.yaml' not found")


key = input("Enter Key: ")


result = requests.get(f"http://localhost:8000/auth/{hwid}/{key}/{get_ip()}")

if result.status_code in [200, 201]:
    with open("auth.yaml", "w") as f:
        yaml.dump({"hwid": hwid, "key": key}, f)

else:
    print("Key not found иди нахуй")

print(result.text)
