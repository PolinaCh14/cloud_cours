import requests
import json

# Backendless API ключі та URL
APP_ID = "1BC26881-9B3B-D569-FF67-A5AF577E5700"
API_KEY = "D1B21117-CEE3-49C8-BF27-BEDD7E928BF8"
BASE_URL = f"https://api.backendless.com/{APP_ID}/{API_KEY}"


def count_user_on_line():
    url = f'{BASE_URL}/services/on_line/count_on_line'
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print(f"Message was sucssesfull create")
    else:
        print(f"Error creating message {response.text}")


def get_amount_of_on_line_users():
    url = f'{BASE_URL}/services/on_line/ge_on_line_users'
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error creating message {response.text}")
        return 0
