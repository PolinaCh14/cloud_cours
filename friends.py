import requests
import json
import math

# Backendless API ключі та URL
APP_ID = "1BC26881-9B3B-D569-FF67-A5AF577E5700"
API_KEY = "D1B21117-CEE3-49C8-BF27-BEDD7E928BF8"
BASE_URL = f"https://api.backendless.com/{APP_ID}/{API_KEY}"


def get_all_users():
    # url = f"{BASE_URL}/data/Friends"
    url = f"{BASE_URL}/data/Users"

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


def get_all_friends_with_user():  # work with user name
    url = f"{BASE_URL}/data/Users?loadRelations=friends"

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


def get_all_users_friends(name):
    url = f"{BASE_URL}/data/Users?loadRelations=friends"

    response = requests.get(url)
    if response.status_code == 200:
        data_user = response.json()
        friends = 0
        for data in data_user:
            if name == data["name"]:
                friends = data["friends"]
                break
        return friends
    else:
        print(
            f"Failed to retrieve posts with authors: {
                response.status_code} - {response.text}"
        )
        return []


def create_friends(user_id, friends_name="", info=0):

    url = f"{BASE_URL}/data/Friends"
    headers = {"Content-Type": "application/json"}
    if info == 0:
        info = {
            "nameFriends": friends_name}
    response = requests.post(url, headers=headers, json=info)

    if response.status_code == 200:
        friends_data = response.json()
        friends_id = friends_data["objectId"]

        relation_url = f"{BASE_URL}/data/Users/{user_id}/friends:Friends:n"

        # Додаємо зв'язок між постом і користувачем
        relation_data = [friends_id]

        response2 = requests.put(
            relation_url, headers=headers, json=relation_data)

        if response2.status_code == 200:
            print("Relation created successfully")
        else:
            print(f"Failed to create relation: {
                  response2.status_code} - {response2.text}")

        return friends_data
    else:
        print(f"Failed to create post: {
              response.status_code} - {response.text}")
        return None


def find_invite_for_user(name):
    url = f"{BASE_URL}/data/Users?loadRelations=friends"

    response = requests.get(url)
    if response.status_code == 200:
        posts_with_authors = response.json()

        # Initialize an empty list to store matching friends
        matching_friends = []

        for user_data in posts_with_authors:

            friends_list = user_data.get("friends", [])
            for friend in friends_list:

                if friend.get("nameFriends") == name and friend.get("status") == "invite":
                    matching_friends.append(user_data)

        return matching_friends
    else:
        print(f"Failed to retrieve posts with authors: {
              response.status_code} - {response.text}")
        return []


def respond_to_invite(user_name, friend_name, user_id, respond):
    tmp = get_all_friends_with_user()
    id_friends_t = 0
    for data in tmp:
        if data["name"] == friend_name:
            friends_list = data.get("friends", [])
            for friend in friends_list:
                if friend.get("nameFriends") == user_name and friend.get("status") == "invite":
                    id_friends_t = friend.get("objectId")
                    break

    url = f"{BASE_URL}/data/Friends/{id_friends_t}"

    headers = {
        'Content-Type': 'application/json',
    }

    if respond:
        new_data = {
            "status": "accepted"
        }
        response = requests.put(url, headers=headers, json=new_data)
        if response.status_code == 200:
            info = {
                "nameFriends": friend_name,
                "status": "accepted"
            }
            create_friends(user_id, info=info)
            return "You have the new friends"
        else:
            return "False"
    new_data = {
        "status": "rejected"
    }
    response = requests.put(url, headers=headers, json=new_data)
    if response.status_code == 200:
        return "Your invite was rejected"
    else:
        return "False"


def find_users(name):
    url = f"{BASE_URL}/data/Users"

    response = requests.get(url)
    res = []
    if response.status_code == 200:
        users = response.json()
        for data in users:
            if name.lower() in data["name"].lower():
                res.append(data)

        return res
    else:
        print(
            f"Failed to list place: {
                response.status_code} - {response.text}"
        )
        return []


def find_users_friend(name_user, name_firends):
    friends = get_all_users_friends(name_user)
    res = []
    for data in friends:
        if name_firends.lower() in data["nameFriends"].lower():
            print(data)
            res.append(data)

    return res


def delete_friends(friends_id, user_name, friend_name):
    url = f"{BASE_URL}/data/Friends/{friends_id}"

    headers = {
        "Content-Type": "application/json",
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print(f"Friends with id {friends_id} was deleted successfully.")
        tmp = get_all_friends_with_user()
        id_friends_t = 0
        for data in tmp:
            if data["name"] == friend_name:
                friends_list = data.get("friends", [])
                for friend in friends_list:
                    if friend.get("nameFriends") == user_name:
                        id_friends_t = friend.get("objectId")
                        break
        if id_friends_t != 0:
            url = f"{BASE_URL}/data/Friends/{id_friends_t}"
            response = requests.delete(url, headers=headers)
            if response.status_code == 200:
                print(f"Friends with id {
                    id_friends_t} was deleted successfully.")
            else:
                print(f"Error delete friends: {response.text}")
        else:
            print("We don't find friend with this name")
    else:
        print(f"Error delete friends: {response.text}")


def haversine_distance2(lat1, lon1, lat2, lon2, radius=6371):

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


def get_friends_on_map(target_lat, target_lon, name):

    radius = 1000
    all_friends = get_all_users_friends(name)
    points_in_radius = {}
    all_user = get_all_users()
    # all_places_dict = {place['objectId']: place for place in all_friends}
    all_places_dict = {}
    for f_data in all_friends:
        for data in all_user:
            if data["name"] == f_data["nameFriends"] and data["share_location"] == True and f_data["status"] == "accepted":
                all_places_dict[data["name"]
                                ] = data["myLocation"]

    for place_id, place_data in all_places_dict.items():
        lat = place_data['coordinates'][1]
        lon = place_data['coordinates'][0]
        distance = haversine_distance2(target_lat, target_lon, lat, lon)
        if distance <= radius:
            points_in_radius[place_id] = place_data

    # print("sdsdsdsd")
    return points_in_radius


# print(get_friends_on_map(51.511092905004745, -0.0569915771484375, "Pon26"))
# print(find_users_friend("Pon26", "Polin"))


# new_data = {
#     "nameFriends": "Polina"
# }
# print(create_friends("14E6B0FA-3BFE-8FE2-FF65-338CF019A500",  new_data))

# print(get_all_users_friends("Pon26"))
# print(delete_friends("EE401CBC-8882-4FD2-AF14-54E9B70B8757", "Pon26", "Pon2"))
# print(find_users("Pon26"))
# print(respond_to_invite("Pon2", "Pon26",
#       "BF3B1B10-188E-04FB-FF84-A24F9E8B7300", True))
