import requests
import json

# Backendless API ключі та URL
APP_ID = "1BC26881-9B3B-D569-FF67-A5AF577E5700"
API_KEY = "D1B21117-CEE3-49C8-BF27-BEDD7E928BF8"
BASE_URL = f"https://api.backendless.com/{APP_ID}/{API_KEY}"


def messages_to_dev_default(status):
    url = f"{BASE_URL}/messaging/default"
    headers = {"Content-Type": "application/json"}
    info = {"message": f'Chek your e-mail, email`s status was {status}',
            "headers": {"status": 'You have a new message'}
            }
    response = requests.post(url, headers=headers,  json=info)
    if response.status_code == 200:
        print(f"Message was sucssesfull create")
    else:
        print(f"Error creating message {response.text}")


def messages_subscribe():
    url = f"{BASE_URL}/messaging/default/subscribe"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print("Message was successfully created.")
        try:
            data = json.loads(response.text)
            subscription_id = data["subscriptionId"]
            return subscription_id
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
        except KeyError as e:
            print(f"Error accessing 'subscriptionId': {e}")
            return None
    else:
        print(f"Error creating message: {response.text}")
        return None


def get_messages():
    res = messages_subscribe()
    url = f"{BASE_URL}/messaging/default/{res}"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # print(response.text)
        data = response.json()  # Парсимо JSON-відповідь
        messages = data.get("messages", [])  # Отримуємо список повідомлень
        message_list = []  # Створюємо список для зберігання статусу та повідомлення
        for message in messages:
            # Отримуємо заголовки повідомлення
            headers = message.get("headers", {})
            status = headers.get("status")  # Отримуємо статус з заголовків
            message_data = message.get("data")  # Отримуємо саме повідомлення
            # Додаємо кортеж до списку
            message_list.append((status, message_data))
        return message_list
    else:
        print(f"Error creating message {response.text}")


def send_message_on_email(status, message):
    url = f"{BASE_URL}/messaging/email"
    headers = {"Content-Type": "application/json"}
    info = {"subject": status, "bodyparts": {
        "textmessage": message}, "to": ["chernyshovapolina014@gmail.com"]}
    response = requests.post(url, headers=headers,  json=info)
    if response.status_code == 200:
        print(f"Message was sucssesfull create")
    else:
        print(f"Error creating message {response.text}")


# print(messages_to_email())


def get_all_message_with_user(user_id):
    url = f"{BASE_URL}/data/Users/{user_id}?loadRelations=letters"

    response = requests.get(url)
    if response.status_code == 200:
        user_with_letters = response.json()
        return user_with_letters
    else:
        print(
            f"Failed to retrieve posts with authors: {
                response.status_code} - {response.text}"
        )
        return []


def create_letter(status, messages):
    url = f"{BASE_URL}/data/Letters"
    headers = {"Content-Type": "application/json"}
    info = {
        "status": status,
        "message": messages}
    response = requests.post(url, headers=headers, json=info)

    if response.status_code == 200:
        lettesr_data = response.json()
        letters_id = lettesr_data["objectId"]

        relation_url = f"{
            BASE_URL}/data/Users/8E93142B-9195-147C-FF1F-63A0D2014400/letters:Letters:n"

        relation_data = [letters_id]
        response2 = requests.put(
            relation_url, headers=headers, json=relation_data)
        if response2.status_code == 200:
            print("Relation created successfully")
        else:
            print(f"Failed to create relation: {
                  response2.status_code} - {response2.text}")

        return lettesr_data
    else:
        print(f"Failed to create post: {
              response.status_code} - {response.text}")
        return None


def delete_letters(letters_id):
    url = f"{BASE_URL}/data/Letters/{letters_id}"

    headers = {
        "Content-Type": "application/json",
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print(f"Letter with id {letters_id} was deleted successfully.")
    else:
        print(f"Error delete letters: {response.text}")


def sort_letters(user_id, type):
    user_data = get_all_message_with_user(user_id)
    list_of_sort_letters = []

    if "letters" in user_data:
        letters_list = user_data["letters"]
        for letter in letters_list:
            if type == letter.get("status"):
                list_of_sort_letters.append(letter)

    return list_of_sort_letters


# print(sort_letters("8E93142B-9195-147C-FF1F-63A0D2014400", "Regret"))
# delete_letters("63BAED9B-5238-4FCC-9635-4C0B54D5A7A3")
# print(create_letter("Hint", "New messijlkdjfdskjf"))
# print(get_all_message_with_user("8E93142B-9195-147C-FF1F-63A0D2014400"))
# messages_to_email()

# 5B18C305-8D04-819E-FF35-B121AAEE0500
# print(messages_to_dev_default("Advd"))
# print(messages_subscribe())
# print(get_messages())
