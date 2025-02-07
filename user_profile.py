import requests
import json
from logging_m import logging_geo_point_error
# Backendless API ключі та URL
APP_ID = "1BC26881-9B3B-D569-FF67-A5AF577E5700"
API_KEY = "D1B21117-CEE3-49C8-BF27-BEDD7E928BF8"
BASE_URL = f"https://api.backendless.com/{APP_ID}/{API_KEY}"


def find_users_pr(user_name):
    url = f"{BASE_URL}/data/Users?where=name%20%3D%20%27{user_name}%27"
    response = requests.get(url)
    if response.status_code == 200:
        user_data = response.json()
        return user_data
    else:
        return False


def get_user_info(user_name):

    url = f"{BASE_URL}/data/Users?where=name%20%3D%20%27{user_name}%27"
    response = requests.get(url)
    if response.status_code == 200:
        user_data = response.json()
        return user_data
    else:
        return []


def edit_user_prifile(user_name, new_data):
    user_info = get_user_info(user_name)
    # if user_info:
    user_data = user_info[0]  # Отримання першого об'єкту зі списку
    headers = {
        'Content-Type': 'application/json',

    }
    url = f'{BASE_URL}/users/{user_data["objectId"]}'
    response = requests.put(url, headers=headers, json=new_data)
    if response.status_code == 200:
        return response.text
        # return True
    else:

        return "((()))"
    # return False


def upload_profile_photo(user_name, file_name):
    url = f"{BASE_URL}/files/users/{user_name}/profile_photo/{file_name}"
    file_name2 = file_name.split("\\")[-1]
    url = f"{BASE_URL}/files/users/{user_name}/profile_photo/{file_name2}"

    with open(file_name, "rb") as file:
        files = {"file": file}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        print(f"File {file_name2} uploaded to Backendless successfully.")
        return url
    else:
        print(
            f"Failed to upload file {file_name} to Backendless: {
                response.status_code} - {response.text}"
        )


def upload_geo(user_name, new_data):
    user_info = get_user_info(user_name)
    # if user_info:
    user_data = user_info[0]  # Отримання першого об'єкту зі списку
    headers = {
        'Content-Type': 'application/json',

    }
    url = f'{BASE_URL}/users/{user_data["objectId"]}'
    response = requests.put(url, headers=headers, json=new_data)
    if response.status_code == 200:
        return response.text
    else:
        logging_geo_point_error(user_data, response.text, user_name)
        return []

# 'myLocation': {'type': 'Point', 'coordinates': [30.62014481, 50.46679663], 'srsId': 4326, '___class': 'com.backendless.persistence.Point'}


# teste = {'myLocation': {
#     "type": "Point",
#     "coordinates": [
#         -3.46633995,
#         42.6449399
#     ]
# }}

# print(upload_geo("Pon2", teste))
# print(get_user_info("Pon26"))
# print(edit_user_prifile("Pon26", r))
# print(check("Pon26"))


# print(upload_profile_photo("Pon2", "D:\\3х4\\me.jpg"))
