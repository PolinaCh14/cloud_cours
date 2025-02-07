from datetime import datetime, timezone, timedelta
import requests
import time
from datetime import datetime


# Backendless API ключі та URL
APP_ID = "1BC26881-9B3B-D569-FF67-A5AF577E5700"
API_KEY = "D1B21117-CEE3-49C8-BF27-BEDD7E928BF8"
BASE_URL = f"https://api.backendless.com/{APP_ID}/{API_KEY}"


current_datetime = datetime.now()
# Конвертуємо дату та час у Unix timestamp з точністю до мілісекунд, враховуючи місцевий часовий пояс
timestamp_ms = current_datetime.replace(tzinfo=timezone.utc).astimezone(
    # Переведення у мілісекунди
    tz=timezone(timedelta(hours=3))).timestamp() * 1000


def logging_authorization_error(user_data, error_m):
    url = f"{BASE_URL}/log"
    headers = {"Content-Type": "application/json"}
    info = [{
        "log-level": "ERROR",
        "logger": "logging_m - logging_authorization_error()",
        "timestamp": timestamp_ms,
        "message": f"{error_m}, with user where {user_data} \n"
    }
    ]
    response = requests.put(url, headers=headers,  json=info)
    if response.status_code == 200:
        print(f"Loggin was sucssesfull create")
    else:
        print(f"Error creating logging {response.text}")


def logging_save_file_error(user_data, error_m):
    url = f"{BASE_URL}/log"
    headers = {"Content-Type": "application/json"}
    info = [{
        "log-level": "ERROR",
        "logger": "logging_m - logging_save_file_error()",
        "timestamp": timestamp_ms,
        "message": f"{error_m}, with {user_data} \n"
    }
    ]
    response = requests.put(url, headers=headers,  json=info)
    if response.status_code == 200:
        print(f"Loggin was sucssesfull create")
    else:
        print(f"Error creating logging {response.text}")


def logging_geo_point_error(user_data, error_m, user_name="None"):
    url = f"{BASE_URL}/log"
    headers = {"Content-Type": "application/json"}
    info = [{
        "log-level": "ERROR",
        "logger": "logging_m - logging_geo_point_error()",
        "timestamp": timestamp_ms,
        "message": f"{error_m}, with {user_name} geo point {user_data} \n"
    }
    ]
    response = requests.put(url, headers=headers,  json=info)
    if response.status_code == 200:
        print(f"Loggin was sucssesfull create")
    else:
        print(f"Error creating logging {response.text}")
