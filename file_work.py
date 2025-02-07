import requests
import json
import os
from logging_m import logging_save_file_error
# Backendless API ключі та URL
APP_ID = "1BC26881-9B3B-D569-FF67-A5AF577E5700"
API_KEY = "D1B21117-CEE3-49C8-BF27-BEDD7E928BF8"
BASE_URL = f"https://api.backendless.com/{APP_ID}/{API_KEY}"


def create_folder(url2, file_name):

    users_index = url2.find("users")

    if users_index != -1:
        # Обрізаємо URL після "users" та повертаємо результат
        user_folder_info = url2[users_index:]
        url = f"{BASE_URL}/files/{user_folder_info}/{file_name}"
    else:
        # Якщо "users" не знайдено, повертаємо порожній рядок
        url = f"{BASE_URL}/files/users/{url2}/{file_name}"

    response = requests.get(url)
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return (f"Folder for user  {
            file_name} created successfully.")
    else:
        return (f"Error creating folder for user {file_name}: {response.text}")


def delete_folder(user_name, folder_name):

    url = f"{BASE_URL}/files/users/{user_name}/{folder_name}"

    headers = {
        "Content-Type": "application/json",
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print(f"Folder for user {user_name} {
              folder_name} deleted successfully.")
    else:
        print(f"Error delete folder for user {folder_name}: {response.text}")


def list_files_in_folder(url2):
    users_index = url2.find("users")

    # Якщо "users" знайдено у URL
    if users_index != -1:
        # Обрізаємо URL після "users" та повертаємо результат
        user_folder_info = url2[users_index:]
    else:
        # Якщо "users" не знайдено, повертаємо порожній рядок
        user_folder_info = ""
    url = f"{BASE_URL}/files/{user_folder_info}"

    response = requests.get(url)
    if response.status_code == 200:
        files = response.json()
        return files
    else:
        print(
            f"Failed to list files in folder {url}: {
                response.status_code} - {response.text}"
        )
        return []

# def list_files_in_folder(user_name, folder_name):
#     url = f"{BASE_URL}/files/users/{user_name}/{folder_name}"

#     response = requests.get(url)
#     files = {}
#     if response.status_code == 200:
#         data = response.json()
#         for file_info in data:
#             if "." not in file_info["name"]:
#                 nested_folder_name = file_info["name"]
#                 nested_files = list_files_in_folder(
#                     user_name, f"{folder_name}/{nested_folder_name}")
#                 files[nested_folder_name] = nested_files
#             else:
#                 files[file_info["name"]] = None
#         # files = response.json()
#         # return files
#         # for file_info in files:
#         #     print(file_info["name"])
#     else:
#         print(
#             f"Failed to list files in folder {folder_name}: {
#                 response.status_code} - {response.text}"
#         )
#         return {}
#     return files


def list_folder2(user_name):
    url = f"{BASE_URL}/files/users/{user_name}"

    response = requests.get(url)
    if response.status_code == 200:
        files = response.json()
        for file_info in files:
            if 'size' in file_info:
                print(True)
            else:
                print(False)
    else:
        print(
            f"Failed to list files in folder {user_name}: {
                response.status_code} - {response.text}"
        )


def list_folder(user_name):
    url = f"{BASE_URL}/files/users/{user_name}"

    response = requests.get(url)
    if response.status_code == 200:
        folders = response.json()
        return folders
    else:
        print(
            f"Failed to list folders for user {user_name}: {
                response.status_code} - {response.text}"
        )
        return []


def get_file_content(url2):
    users_index = url2.find("users")

    # Якщо "users" знайдено у URL
    if users_index != -1:
        # Обрізаємо URL після "users" та повертаємо результат
        user_folder_info = url2[users_index:]
    else:
        # Якщо "users" не знайдено, повертаємо порожній рядок
        user_folder_info = ""
    url = f"{BASE_URL}/files/{user_folder_info}"

    response = requests.get(url)
    if response.status_code == 200:
        if isinstance(response.content, str):
            return response.text
    # Отримання байтового вмісту
        elif isinstance(response.content, bytes):
            return response.content
        # file_content = response.content
        # print(f"File content for {file_name}:")
        # print(file_content)
        # return file_content
    else:
        print(
            f"Failed to get file content for {url2}: {
                response.status_code} - {response.text}"
        )
        return ""


# def upload_file_to_(url2, file_name):
#     users_index = url2.find("users")
#     if users_index != -1:
#         # Обрізаємо URL після "users" та повертаємо результат
#         user_folder_info = url2[users_index:]
#     else:
#         # Якщо "users" не знайдено, повертаємо порожній рядок
#         user_folder_info = ""

#     # url = f"{BASE_URL}/files/users/{user_name}/{folder_name}/{file_name}"
#     file_name2 = file_name.split("\\")[-1]
#     url = f"{BASE_URL}/files/{user_folder_info}/{file_name2}"
#     with open(file_name, "rb") as file:
#         files = {"file": file}
#         response = requests.post(url, files=files)

#     if response.status_code == 200:
#         print(f"File {file_name2} uploaded to Backendless successfully.")
#     else:
#         logging_save_file_error(file_name, response.text)
#         print(
#             f"Failed to upload file {file_name} to Backendless: {
#                 response.status_code} - {response.text}"
#         )


def upload_file_to_(url2, file_name):
    users_index = url2.find("users")
    if users_index != -1:
        # Обрізаємо URL після "users" та повертаємо результат
        user_folder_info = url2[users_index:]
    else:
        # Якщо "users" не знайдено, повертаємо порожній рядок
        user_folder_info = ""

    # url = f"{BASE_URL}/files/users/{user_name}/{folder_name}/{file_name}"
    file_name2 = file_name.split("\\")[-1]
    url = f"{BASE_URL}/files/{user_folder_info}/{file_name2}"

    try:
        with open(file_name, "rb") as file:
            files = {"file": file}
            response = requests.post(url, files=files)

        if response.status_code == 200:
            print(f"File {file_name2} uploaded to Backendless successfully.")
        else:
            logging_save_file_error(file_name, response.text)
            print(
                f"Failed to upload file {file_name} to Backendless: {
                    response.status_code} - {response.text}"
            )
    except Exception as e:
        logging_save_file_error(file_name, str(e))
        print(f"An error occurred: {e}")


def download_file_from(url2):
    users_index = url2.find("users")

    # Якщо "users" знайдено у URL
    if users_index != -1:
        # Обрізаємо URL після "users" та повертаємо результат
        user_folder_info = url2[users_index:]
    else:
        # Якщо "users" не знайдено, повертаємо порожній рядок
        user_folder_info = ""
    url = f"{BASE_URL}/files/{user_folder_info}"
    # url = f"{BASE_URL}/files/users/{user_name}/{folder_name}/{file_name}"
    file_name = url.split("/")[-1]
    response = requests.get(url)
    if response.status_code == 200:
        with open((f"d:/{file_name}"), "wb") as file:
            file.write(response.content)
        return (f"File {file_name} downloaded from Backendless to  successfully.")
    else:
        return (
            f"Failed to download file {file_name} from Backendless: {
                response.status_code} - {response.text}"
        )


def delete_file(url2):
    users_index = url2.find("users")

    # Якщо "users" знайдено у URL
    if users_index != -1:
        # Обрізаємо URL після "users" та повертаємо результат
        user_folder_info = url2[users_index:]
    else:
        # Якщо "users" не знайдено, повертаємо порожній рядок
        user_folder_info = ""
    url = f"{BASE_URL}/files/{user_folder_info}"
    # url = f"{BASE_URL}/files/users/{user_name}/{folder_name}/{file_name}"
    file_name = url.split("/")[-1]
    response = requests.get(url)
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.delete(url, headers=headers)
    # if response.status_code == 200:
    #     return (f"Folder for user {file_name} deleted successfully.")
    # else:
    #     return (f"Error delete folder for user {file_name}: {response.text}")


def check(user_name):
    url = f"{BASE_URL}/data/Users?where=name%20%3D%20%27{user_name}%27"
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False


def give_file_to_another(url, second_user):
    file_name = url.split("/")[-1]
    url3 = f"{BASE_URL}/files/append/users/{second_user}/shared-with-me/{file_name}"

    if check(second_user):
        try:
            add_url(url3, url)
        except requests.exceptions.HTTPError as err:
            print("Error creating file:", err)

    else:
        print("Користувач не знайдений.")
    # add_url(url3, url)


# def give_file_to_another(user_name, folder_name, file_name, second_user):
#     url = f"{BASE_URL}/files/users/{user_name}/{folder_name}/{file_name}"
#     url3 = f"{BASE_URL}/files/append/users/{second_user}/shared-with-me/{file_name}"
#     file_name2 = url.split("/")[-1]
#     if check(second_user):
#         try:
#             print("Ddd")
#             add_url(url3, url)
#         except requests.exceptions.HTTPError as err:
#             print("Error creating file:", err)

#     else:
#         print("Користувач не знайдений.")


def add_url(url, url2):
    try:
        headers = {"Content-Type": "text/plain"}

        response = requests.put(url, headers=headers, data=url2)
        response.raise_for_status()

        print("Дані успішно записано в файл:", response.text)
    except requests.exceptions.HTTPError as err:
        print("Помилка при записі даних в файл:", err)


def read_file_and_follow_link(file_path):
    try:
        response = requests.get(file_path)
        if response.text.startswith("http"):
            # Перейти за посиланням
            response = requests.get(response.text)

            # Перевірити статус відповіді
            if response.status_code == 200:
                # Отримати вміст файлу за посиланням
                file_content = response.text

                # Обробити вміст файлу, наприклад, вивести його на екран
                print("Зміст файлу, на який посилається посилання:")
                return file_content
            else:
                print("Не вдалося завантажити файл за посиланням.")
        else:
            print("У файлі не знайдено посилання.")
    except FileNotFoundError:
        print("Файл не знайдено.")
    except Exception as e:
        print("Виникла помилка:", e)

# def download_file_from(user_name, folder_name, file_name):
#     url = f"{BASE_URL}/files/users/{user_name}/{folder_name}/{file_name}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         with open((f"d:/nure/{file_name}"), "wb") as file:
#             file.write(response.content)
#         print(
#             f"File {file_name} downloaded from Backendless to {
#                 folder_name} successfully."
#         )
#     else:
#         print(
#             f"Failed to download file {file_name} from Backendless: {
#                 response.status_code} - {response.text}"
#         )


def download_file_from_file(file_path):
    try:
        response = requests.get(file_path)
        if response.text.startswith("http"):
            # Перейти за посиланням
            response = requests.get(response.text)
            file_name = file_path.split("/")[-1]
            # Перевірити статус відповіді
            if response.status_code == 200:
                # Отримати вміст файлу за посиланням
                with open((f"d:/{file_name}"), "wb") as file:
                    file.write(response.content)
                    return (
                        f"File {file_name} downloaded from Backendless successfully.")
            else:
                return ("Не вдалося завантажити файл за посиланням.")
        else:
            print("У файлі не знайдено посилання.")
    except FileNotFoundError:
        print("Файл не знайдено.")


# print(check("Pon26"))


# Приклад використання:
# Ім'я файлу
# file_url = get_file_url("Pon26", "test_folder", "test3.txt")
# if file_url:
#     print("URL файлу:", file_url)

# ******************************************************************
# create_folder("Pon26", "test_folder22")


# delete_folder("Pon26", "test_folder22")
# list_files_in_folder("Pon26", "test_folder")
# get_file_content("Pon2", "shared-with-me", "test3.txt")
# upload_file_to_("Pon26", "test_folder", r"D:\3х4\20230605_164946.jpg")
# download_file_from("Pon26", "test_folder", "test.txt")
# delete_file("Pon26", "test_folder", "test.txt")
# print(check("Pon26"))
# give_file_to_another("Pon26", "test_folder", "test3.txt", "Pon2")
# get_file_content("Pon2", "shared-with-me", "test3.txt")
# url = f"{BASE_URL}/files/users/Pon26/test_folder/test3.txt"
# "https://finestsoap.backendless.app/api/files/users/Pon2/shared-with-me/test3.txt"
# url3 = f"{BASE_URL}/files/append/users/Pon2/shared-with-me/test3.txt"
# url3 = f"{BASE_URL}/files/append/users/Pon2/shared-with-me/test3.txt"
# ur
# add_url(url3, url)
# # print(custom_find_by_name())
# print(custom_find_by_name1())
# print(check("Pon26"))


# read_file_and_follow_link(
#     f"{BASE_URL}/files/users/Pon2/shared-with-me/test3.txt")


# download_file_from_file(
#     f"{BASE_URL}/files/users/Pon2/shared-with-me/test3.txt")


# print(list_folder2("Pon26"))
