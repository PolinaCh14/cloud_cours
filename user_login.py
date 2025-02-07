import requests
from logging_m import logging_authorization_error


# Backendless API ключі та URL
APP_ID = "1BC26881-9B3B-D569-FF67-A5AF577E5700"
API_KEY = "D1B21117-CEE3-49C8-BF27-BEDD7E928BF8"
BASE_URL = f"https://api.backendless.com/{APP_ID}/{API_KEY}"


def register_user(email, password, name, age, gender, country):
    url = f"{BASE_URL}/users/register"
    headers = {"Content-Type": "application/json"}
    if age <= 5:
        error_message = "Age must be at least 5 years old."
        return {"success": False, "message": error_message}

    data = {
        "email": email,
        "password": password,
        "name": name,
        "age": age,
        "gender": gender,
        "country": country,
    }
    response = requests.post(url, headers=headers, json=data)
    try:
        if response.status_code == 200:
            user_data = response.json()
            # user_id = user_data["name"]
            if 'name' in user_data:
                user_id = user_data['name']
                create_user_folder(user_id)
            # create_user_folder(user_id)
            return {
                "success": True,
                "message": "User registered successfully.",
                "data": response.json(),
            }
        else:
            error_message = response.json().get("message") or response.json().get(
                "errorData"
            )
            return {
                "success": False,
                "message": f"Error registering user: {error_message}",
            }
    except Exception as e:
        return {"success": False, "message": f"Error: {e}"}


def login_user(email, password):
    url = f"{BASE_URL}/users/login"
    headers = {"Content-Type": "application/json"}
    data = {"login": email, "password": password}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        user_data = response.json()
        # user_id = user_data["name"]
        return {
            "success": True,
            "message": "User registered successfully.",
            "data": response.json(),
        }
    else:
        error_message = response.json().get("message") or response.json().get(
            "errorData"
        )
        logging_authorization_error(data, error_message)
        # print(error_message)
        return {
            "success": False,
            "message": f"Error registering user: {error_message}",
        }


def reset_password(loggin):
    url = f"{BASE_URL}/users/restorepassword/{loggin}"
    response = requests.get(url)
    return response.json()


def create_user_folder(user_id):
    # Ваш код для створення папки для користувача за його ідентифікатором user_id
    url = f"{BASE_URL}/files/users/{user_id}"
    url2 = f"{BASE_URL}/files/users/{user_id}/shared-with-me"
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers)
    response2 = requests.post(url2, headers=headers)
    if response.status_code == 200:
        print(f"Folder for user {user_id} created successfully.")
    else:
        print(f"Error creating folder for user {user_id}: {response.text}")


# Приклад використання функцій:
# register_response = register_user(
#     "chernyshovh4@gmail.com", "password112", "Pon26", 12, "m", "Ukrain"
# )
# print(register_response)

# login_response = login_user("Polinnn", "lsEM4Lcx")
# print(login_response)

# reset_password_response = reset_password("Polinnn")
# print(reset_password_response)
