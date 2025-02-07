import requests
import json
import math

# Backendless API ключі та URL
APP_ID = "1BC26881-9B3B-D569-FF67-A5AF577E5700"
API_KEY = "D1B21117-CEE3-49C8-BF27-BEDD7E928BF8"
BASE_URL = f"https://api.backendless.com/{APP_ID}/{API_KEY}"


def upload_place_photo(user_name, file_name):
    # url = f"{BASE_URL}/files/users/{user_name}/place_photo/{file_name}"
    file_name2 = file_name.split("\\")[-1]
    url = f"{BASE_URL}/files/users/{user_name}/place_photo/{file_name2}"

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


def get_all_place():
    url = f"{BASE_URL}/data/Place"

    response = requests.get(url)
    if response.status_code == 200:
        place = response.json()
        return place
    else:
        print(
            f"Failed to list place: {
                response.status_code} - {response.text}"
        )
        return []


def get_all_place_with_user():  # work with user name
    url = f"{BASE_URL}/data/Users?loadRelations=place_post"

    response = requests.get(url)
    if response.status_code == 200:
        posts_with_authors = response.json()
        # [0].get("place_post")
        return posts_with_authors
    else:
        print(
            f"Failed to retrieve posts with authors: {
                response.status_code} - {response.text}"
        )
        return []


def create_place(user_id, info):

    url = f"{BASE_URL}/data/Place"
    headers = {"Content-Type": "application/json"}

    # Створюємо пост
    response = requests.post(url, headers=headers, json=info)

    if response.status_code == 200:
        post_data = response.json()
        post_id = post_data["objectId"]

        # Отримуємо URL для створення зв'язку між постом і користувачем
        # relation_url = f"{
        #     BASE_URL}/data/Users/{user_id}?place_post"
        # relation_url = f"{BASE_URL}/data/Users/{user_id}"
        relation_url = f"{BASE_URL}/data/Users/{user_id}/place_post:Post:n"

        # Додаємо зв'язок між постом і користувачем
        relation_data = [post_id]

        response2 = requests.put(
            relation_url, headers=headers, json=relation_data)

        if response2.status_code == 200:
            print("Relation created successfully")
        else:
            print(f"Failed to create relation: {
                  response2.status_code} - {response2.text}")

        return post_data
    else:
        print(f"Failed to create post: {
              response.status_code} - {response.text}")
        return None


# def get_place_by_user_name(user_name):
#     url = f"{BASE_URL}/data/Place?where=user_name%20%3D%20%27{user_name}%27"
#     response = requests.get(url)
#     if response.status_code == 200:
#         result = response.json()
#         return result
#     else:
#         return "False"

def get_place_by_user_name(user_name):
    # GET http://xxxx.backendless.app/data/[TABLE-NAME]?loadRelations=[RELATED-PROPERTY-NAME]
    url = f"{BASE_URL}/data/Place?where=user_name%20%3D%20%27{user_name}%27"
    # url = f"{
    #     BASE_URL}/data/Users?{user_name}loadRelations=place_post"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return []


def find_users_id(user_name):
    url = f"{BASE_URL}/data/Users?where=name%20%3D%20%27{user_name}%27"
    response = requests.get(url)
    if response.status_code == 200:
        user_data = response.json()
        return user_data[0]["objectId"]
        # return response.text
    else:
        return False


def delete_place(place_id):
    url = f"{BASE_URL}/data/Place/{place_id}"

    headers = {
        "Content-Type": "application/json",
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print(f"Place {place_id} deleted successfully.")
    else:
        print(f"Error delete place: {response.text}")


def get_location_info(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={
        latitude}&lon={longitude}&format=json&accept-language=en"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city = data.get("address", {}).get("city")
        state = data.get("address", {}).get("state"),
        country = data.get("address", {}).get("country")
        return f"{city}, {state}, {country}"

    else:
        return None


# def add_like(name, place_id):
#     url = f"{BASE_URL}/data/Place/{place_id}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         print("ddd")
#         num_l = int(data["num_likes"])
#         num_l += 1
#         like = data["likes"]
#         like.append(name)
#         relation_data = {
#             "num_likes": num_l,
#             "liks": like
#         }
#         headers = {
#             "Content-Type": "application/json",
#         }
#         response2 = requests.put(
#             url, headers=headers, json=relation_data)

#         if response2.status_code == 200:
#             print("Relation created successfully")
#         else:
#             print(f"Failed to create relation: {
#                   response2.status_code} - {response2.text}")

#     return None


def add_likes(name, place_id):
    url = f"{BASE_URL}/data/Place/{place_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        num_l = int(data["num_likes"])
        num_l += 1
        # Отримати значення поля 'likes' або пустий список, якщо поле не існує
        like = data["likes"]
        if like is None:
            like = [name]
        else:
            like.append(name)
        relation_data = {
            "num_likes": num_l,
            "likes": like  # Виправлено орфографічну помилку 'liks' на 'likes'
        }
        headers = {
            "Content-Type": "application/json",
        }
        response2 = requests.put(
            url, headers=headers, json=relation_data)

        if response2.status_code == 200:
            print("Like added successfully")
        else:
            print(f"Failed to create relation: {
                  response2.status_code} - {response2.text}")

    return None


# def find_by_place_name(place_name):
#     all_p = get_all_place()
#     # print(all_p)
#     ress = []
#     for i in all_p:
#         print(all_p[i])
#         # print(i)
#         # print(" ")
#         # if place_name in all_p[i]
#         #     ress.append(i)

#     return ress
# Припустимо, що у вас є функція get_all_place(), яка повертає список об'єктів місць.

def find_by_place_name(place_name):
    all_places = get_all_place()  # Повертає список усіх місць

    # Перетворюємо список у словник, використовуючи 'objectId' як ключ
    all_places_dict = {place['objectId']: place for place in all_places}

    results = []

    for place_id, place_data in all_places_dict.items():
        # Припустимо, що назва місця зберігається під ключем "text_location"
        text_location = place_data.get("text_location")
        if text_location is not None and place_name.lower() in text_location.lower():
            results.append(place_data)

    return results


def find_by_hashtag(place_name):
    all_places = get_all_place()  # Повертає список усіх місць

    # Перетворюємо список у словник, використовуючи 'objectId' як ключ
    all_places_dict = {place['objectId']: place for place in all_places}

    results = []

    for place_id, place_data in all_places_dict.items():
        # Перевіряємо, чи є поле 'hashtag' не None
        hashtags = place_data.get("hashtag")
        if hashtags is not None:
            # Якщо поле 'hashtag' не None, перевіряємо кожний 'hashtag'
            for hashtag in hashtags:
                if place_name.lower() in hashtag.lower():
                    results.append(place_data)
                    break  # Якщо знайдено збіг, можна виходити з циклу

    return results


def haversine_distance(lat1, lon1, lat2, lon2, radius=6371):
    """
    Обчислює відстань між двома точками на поверхні сфери за допомогою формули Гаверсіна.

    Параметри:
    lat1, lon1: float, широта та довгота першої точки в градусах
    lat2, lon2: float, широта та довгота другої точки в градусах
    radius: float, радіус сфери (за замовчуванням, радіус Землі у кілометрах)

    Повертає:
    float, відстань між двома точками у кілометрах
    """
    # Переведення градусів у радіани
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Різниця широти та довготи
    d_lat = lat2 - lat1
    d_lon = lon2 - lon1

    # Обчислення відстані за формулою Гаверсіна
    a = math.sin(d_lat / 2)**2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(d_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c

    return distance


def find_points_in_radius(target_lat, target_lon):

    radius = 800
    all_places = get_all_place()
    points_in_radius = []
    all_places_dict = {place['objectId']: place for place in all_places}

    for place_id, place_data in all_places_dict.items():
        lat = place_data['location_p']['coordinates'][1]
        lon = place_data['location_p']['coordinates'][0]
        distance = haversine_distance(target_lat, target_lon, lat, lon)
        if distance <= radius:
            points_in_radius.append(place_data)

    # print("sdsdsdsd")
    return points_in_radius


# ress = find_points_in_radius(21.884765625, 38.89103282648846)
# for i in ress:
#     print(i, sep="\n")


# print(find_by_hashtag("op"))

# print(add_like("Pon2", "08C83458-5DBF-4EEF-AD2B-CFFAA6B4AAF3"))
# latitude = 38.78124012
# longitude = 21.91177517
# location_info = get_location_info(latitude, longitude)
# print(location_info)
# def create_place(info):
#     url = f"{BASE_URL}/data/Place"
#     url2 = f"{BASE_URL}/data/Users"

#     headers = {"Content-Type": "application/json"}

#     response = requests.post(url, headers=headers, json=info)
#     if response.status_code == 200:
#         post = response.json()
#         headers = {"Content-Type": "application/json"}
#         info2 = {"place_post": post[0]["objectId"]}
#         response2 = requests.post(url2, headers=headers, json=info2)
#         if response2.status_code == 200:
#             print("Slkdnas;lj")

#         return post
#     else:
#         print(
#             f"Failed to create post: {
#                 response.status_code} - {response.text}"
#         )
#         return []


# info = {
#     'location_p': {
#         "type": "Point",
#         "coordinates": [
#                 -3.46633995,
#                 42.6449399
#         ]
#     },
#     "text_p": "dsfhsdkfjhsdkfhdsfj",
#     "hashtag": ["ekfslkdfdskjf"],
#     "user_name": "Pon2",
# }

# print(get_all_place_with_user())
# "14E6B0FA-3BFE-8FE2-FF65-338CF019A500"
# "8E93142B-9195-147C-FF1F-63A0D2014400"

# print(create_place("8E93142B-9195-147C-FF1F-63A0D2014400", info))


# print(get_place_by_user_name("14E6B0FA-3BFE-8FE2-FF65-338CF019A500"))
# print(delete_place("7D03EEFF-2485-4C76-9335-FDE9C34BDAC5"))
