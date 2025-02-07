from flask import request
from flask import Flask
from flask import render_template
from flask import request, jsonify
from flask import url_for
from flask import session
from flask import redirect
from user_login import *
from file_work import *
from os.path import splitext
from user_profile import *
from place_user import *
from friends import *
from datetime import datetime
from messages import *
from service_r import *

app = Flask(__name__, template_folder="template")
app.config["SECRET_KEY"] = "xfDwsAuM7xXROnBiqkV3fQ"
name = ""
res2 = 0
friends2 = 0


@app.context_processor
def inject_messages():
    message_list = get_messages()
    name = session.get('username')
    return dict(list_m=message_list, name=name)


@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        global name
        name = request.form['name']
        age = int(request.form['age'])
        gender = request.form['gender']
        country = request.form['country']

        registration_result = register_user(
            email, password, name, age, gender, country)
        print(registration_result)
        print("Sss")
        if registration_result['success']:
            print("Ss2")
            session['username'] = name
            count_user_on_line()
            return redirect(url_for('edit_user_loc'))
        else:
            error_message = registration_result['message']
            return render_template('register.html', error_message=error_message)
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def loggin():
    if request.method == 'POST':
        password = request.form['password']

        name = request.form['name']

        login_result = login_user(name, password)

        if login_result['success']:
            session['username'] = name
            count_user_on_line()
            return redirect(url_for('edit_user_loc'))
        else:
            error_message = login_result['message']
            return render_template('login.html', error_message=error_message)
    else:
        return render_template('login.html')


@app.route('/new_password', methods=['GET', 'POST'])
def new_password():
    if request.method == 'POST':

        login = request.form['name']

        reset_password(login)

        return render_template('login.html')
    else:
        return render_template('new-password.html')


@app.route("/main")
def index():
    # name = session.get('username')
    # message_list = get_messages()
    # print(message_list)
    return render_template("index.html")
    # return render_template("index.html", list_m=message_list, name=name)


@app.route("/folders")
def folders():
    name = session.get('username')
    if name:
        folders = list_folder(name)
        return render_template("folders1.html", folders=folders)
    else:
        # Якщо ім'я користувача не збережено в сеансі, перенаправте його на сторінку авторизації
        return redirect(url_for('loggin'))


@app.route("/<path:folder_name>")
def folder(folder_name):
    name = session.get('username')
    if name:
        folders = list_files_in_folder(folder_name)
        return render_template("folder2.html", folders=folders)
    else:
        # Якщо ім'я користувача не збережено в сеансі, перенаправте його на сторінку авторизації
        return redirect(url_for('loggin'))


@app.route("/getFileContent/<path:folder_contents>")
def getFileContent(folder_contents):
    name = session.get('username')
    if name:
        folders = get_file_content(folder_contents)
        # return render_template("file-content.html", folders=folders)
        is_image = False
        if isinstance(folders, bytes):
            # Якщо вміст файлу - байти, перевіряємо наявність розширення зображення
            _, extension = splitext(folder_contents)
            is_image = extension.lower() in ['.jpg', '.jpeg', '.png']
        return render_template("file-content.html", folders=folders, is_image=is_image)

    else:
        # Якщо ім'я користувача не збережено в сеансі, перенаправте його на сторінку авторизації
        return redirect(url_for('loggin'))


@app.route("/download/<path:folder_contents>")
def download(folder_contents):
    name = session.get('username')
    if name:
        folders = download_file_from(folder_contents)
        # return render_template("file-content.html", folders=folders)

        return render_template("download.html", folders=folders)

    else:
        # Якщо ім'я користувача не збережено в сеансі, перенаправте його на сторінку авторизації
        return redirect(url_for('loggin'))


@app.route("/delete_f/<path:folder_contents>")
def delete_f(folder_contents):
    name = session.get('username')
    if name:
        folders = delete_file(folder_contents)
        # return render_template("file-content.html", folders=folders)

        return redirect(url_for("folders"))
    else:
        # Якщо ім'я користувача не збережено в сеансі, перенаправте його на сторінку авторизації
        return redirect(url_for('loggin'))


@app.route("/create_mf", methods=("GET", "POST"))
def create_mf():
    name = session.get('username')
    if request.method == "POST":
        file_name = request.form["name"]
        if name:
            folders = create_folder(name, file_name)
        # return render_template("file-content.html", folders=folders)
            # return render_template("delete.html", folders=folders)
            print(folders)
            return redirect(url_for("folders"))

        else:
            # Якщо ім'я користувача не збережено в сеансі, перенаправте його на сторінку авторизації
            return redirect(url_for('loggin'))

    return render_template("create-folder.html")


@app.route("/create_f/<path:folder_contents>", methods=("GET", "POST"))
def create_f(folder_contents):
    name = session.get('username')
    if request.method == "POST":
        file_name = request.form["name"]
        if name:
            folders = create_folder(folder_contents, file_name)
        # return render_template("file-content.html", folders=folders)
            # return render_template("delete.html", folders=folders)
            print(folders)
            return redirect(url_for("folders"))

        else:
            # Якщо ім'я користувача не збережено в сеансі, перенаправте його на сторінку авторизації
            return redirect(url_for('loggin'))

    return render_template("create-folder.html")


@app.route("/share_with/<path:folder_contents>", methods=("GET", "POST"))
def share_with(folder_contents):
    name = session.get('username')
    if request.method == "POST":
        user_name = request.form["name"]
        if name:
            folders = give_file_to_another(folder_contents, user_name)
        # return render_template("file-content.html", folders=folders)
            # return render_template("delete.html", folders=folders)
            print(folders)
            return redirect(url_for("folders"))

        else:
            # Якщо ім'я користувача не збережено в сеансі, перенаправте його на сторінку авторизації
            return redirect(url_for('loggin'))

    return render_template("share.html")


@app.route("/getFileContentFromShare/<path:folder_contents>")
def getFileContentFromShare(folder_contents):
    name = session.get('username')
    if name:
        folders = read_file_and_follow_link(folder_contents)
        # return render_template("file-content.html", folders=folders)
        is_image = False
        if isinstance(folders, bytes):
            # Якщо вміст файлу - байти, перевіряємо наявність розширення зображення
            _, extension = splitext(folder_contents)
            is_image = extension.lower() in ['.jpg', '.jpeg', '.png']
        return render_template("file-content.html", folders=folders, is_image=is_image)

    else:
        # Якщо ім'я користувача не збережено в сеансі, перенаправте його на сторінку авторизації
        return redirect(url_for('loggin'))


@app.route("/download_from_file/<path:folder_contents>")
def download_from_file(folder_contents):
    name = session.get('username')
    if name:
        folders = download_file_from_file(folder_contents)
        # return render_template("file-content.html", folders=folders)

        return render_template("download.html", folders=folders)

    else:
        # Якщо ім'я користувача не збережено в сеансі, перенаправте його на сторінку авторизації
        return redirect(url_for('loggin'))


@app.route("/download_file_to/<path:folder_contents>", methods=("GET", "POST"))
def download_file_to(folder_contents):
    name = session.get('username')
    if request.method == "POST":
        file_path = request.form["path"]
        if name:
            folders = upload_file_to_(folder_contents, file_path)
        # return render_template("file-content.html", folders=folders)
            # return render_template("delete.html", folders=folders)
            print(folders)
            return redirect(url_for("folders"))

        else:
            # Якщо ім'я користувача не збережено в сеансі, перенаправте його на сторінку авторизації
            return redirect(url_for('loggin'))

    return render_template("download-file.html")


@app.route("/user_profile")
def user_profile():
    name = session.get('username')
    if name:
        user_info = get_user_info(name)
        return render_template("profile-user.html", user_info=user_info)
    else:
        return redirect(url_for('loggin'))


@app.route("/edit_user", methods=("GET", "POST"))
def edit_user():
    name = session.get('username')
    user_d = get_user_info(name)
    if request.method == "POST":

        new_mainPhoto = request.form["mainPhoto"]
        new_country = request.form["country"]
        new_gender = request.form["gender"]
        new_loc = request.form["location"]
        if new_loc == "true":
            new_loc = True
        elif new_loc == "false":
            new_loc = False

        current_mainPhoto = user_d[0]["mainPhoto"]

        current_country = user_d[0]["country"]
        current_gender = user_d[0]["gender"]
        current_log = user_d[0]["share_location"]

        new_data = {}
        if new_mainPhoto != current_mainPhoto:
            new_ph = upload_profile_photo(name, new_mainPhoto)

            new_data["mainPhoto"] = new_ph
        if new_country != current_country:
            new_data["country"] = new_country
        if new_gender != current_gender:
            new_data["gender"] = new_gender
        if new_loc != current_log:
            new_data["share_location"] = new_loc

        # Оновлення даних, якщо вони були змінені
        if new_data:
            edit_user_prifile(name, new_data)

        # Після оновлення або якщо дані не були змінені, перенаправляємо на профіль користувача
        return redirect(url_for("user_profile"))

    return render_template("edit-user.html", user_d=user_d)


@app.route("/edit_user_loc", methods=("GET", "POST"))
def edit_user_loc():
    name = session.get('username')
    if request.method == "POST":
        # Отримання нових даних з запиту
        data = request.get_json()
        lat = data.get("lat")
        lng = data.get("lng")

        # Перевірка на наявність даних та їх оновлення
        if lat is not None and lng is not None:
            new_data = {
                'myLocation': {
                    "type": "Point",
                    "coordinates": [
                        float(lng),
                        float(lat)
                    ]
                }
            }

            upload_geo(name, new_data)

            return jsonify({"message": "Координати успішно оновлені"})
        else:
            return jsonify({"error": "Помилка: неправильні дані координат"}), 400

    return render_template("location-user.html")


@app.route("/all_place", methods=("GET", "POST"))
def all_place():
    name = session.get('username')
    if request.method == "POST":
        word = request.form["word"]
        check = request.form["check"]
        res = 0
        if check == "location":
            res = find_by_place_name(word)
            return render_template("place.html", places=res, name_us=name)
        else:
            res = find_by_hashtag(word)
            return render_template("place.html", places=res, name_us=name)

    if name:
        places = get_all_place()
        return render_template("place.html", places=places, name_us=name)
    else:
        return redirect(url_for('loggin'))


@app.route("/all_user_place")
def all_user_place():
    name = session.get('username')
    if name:
        places = get_place_by_user_name(name)
        return render_template("user-place.html", places=places, name_us=name)
    else:
        return redirect(url_for('loggin'))


@app.route("/place_on_map/<float:latitude>/<float:longitude>")
def place_on_map(latitude, longitude):
    name = session.get('username')
    if name:
        return render_template("place_on_map.html", latitude=latitude, longitude=longitude)
    else:
        return redirect(url_for('loggin'))


@app.route("/delete_us_place/<string:place_id>")
def delete_us_place(place_id):
    name = session.get('username')
    if name:
        delete_place(place_id)
        return redirect(url_for('all_place'))

    redirect(url_for('loggin'))


@app.route("/create_user_place", methods=("GET", "POST"))
def create_user_place():
    name = session.get('username')
    user_id = find_users_id(name)
    if request.method == "POST":
        # Отримуємо дані з запиту
        lat = request.form.get("lat")
        lng = request.form.get("lng")
        hashtag = request.form.get("hashtag")
        hashtag = hashtag.split(", ")
        photo_pot = request.form.get("photo_pot")
        print(photo_pot)
        if photo_pot is "" or photo_pot == "Your photo":
            photo_pot = None
        else:
            photo_pot = upload_place_photo(name, photo_pot)
        text_p = request.form.get("text_p")
        print(photo_pot)

        # Отримання додаткових даних з форми
        current_date = str(datetime.now().date())
        text_location = get_location_info(float(lat), float(lng))
        new_data = {
            "text_location": text_location,
            "user_name": name,
            "hashtag": hashtag,
            "location_p": {
                "type": "Point",
                "coordinates": [
                        float(lng),
                        float(lat)
                ]
            },
            "photo_pot": photo_pot,
            "text_p": text_p,
            "str_date": str(current_date)
        }

        if new_data:
            create_place(user_id, new_data)

        return redirect(url_for("all_user_place"))

    return render_template("create-user-place.html")


@app.route("/add_like/<string:place_id>")
def add_like(place_id):
    name = session.get('username')
    if name:
        add_likes(name, place_id)
        return redirect(url_for('all_place'))

    redirect(url_for('loggin'))


# @app.route("/find_on_map", methods=("GET", "POST"))
# def find_on_map():
#     name = session.get('username')
#     user_d = find_users_pr(name)
#     if request.method == "POST":
#         # Отримання нових даних з запиту
#         data = request.get_json()
#         lat = data.get("lat")
#         lng = data.get("lng")

#         res = find_points_in_radius(float(lat), float(lng))
#         return render_template("place.html", places=res, name_us=name)

#     return render_template("find-on-map.html")
@app.route("/find_on_map", methods=("GET", "POST"))
def find_on_map():
    name = session.get('username')
    # user_d = get_user_info(name)
    if request.method == "POST":
        data = request.get_json()
        lat = float(data.get("lat"))
        lng = float(data.get("lng"))

        # Фільтруємо пости за отриманими координатами
        global res2
        res2 = find_points_in_radius(lat, lng)
        # return render_template("place.html", places=res2, name_us=name)

    return render_template("find-on-map.html")


@app.route("/place_on_map2", methods=("GET", "POST"))
def place_on_map2():
    name = session.get('username')
    if name:
        return render_template("place.html", places=res2, name_us=name)

    redirect(url_for('loggin'))


@app.route("/all_friends",  methods=("GET", "POST"))
def all_friends():
    name = session.get('username')
    if request.method == "POST":
        word = request.form["word"]
        check = request.form["check"]
        res = 0
        if check == "users":
            res = find_users(word)
            return render_template("find_user.html", users=res)
        else:
            res = find_users_friend(name, word)
            return redirect(url_for('all_friends'))

    if name:
        friends = get_all_users_friends(name)
        amount = get_amount_of_on_line_users()
        return render_template("friends.html", friends=friends, amount=amount)
    else:
        # Якщо ім'я користувача не збережено в сеансі, перенаправте його на сторінку авторизації
        return redirect(url_for('loggin'))


@app.route("/delete_u_friends/<string:friends_id>/<string:friends_name>")
def delete_u_friends(friends_id, friends_name):
    name = session.get('username')
    if name:
        delete_friends(friends_id, name, friends_name)
        return redirect(url_for('all_friends'))
    else:
        return redirect(url_for('loggin'))


@app.route("/invite_user/<string:user_name>")
def invite_user(user_name):
    name = session.get('username')
    if name:
        user_id = find_users_id(name)
        create_friends(user_id, user_name)
        return redirect(url_for('all_friends'))
    else:
        return redirect(url_for('loggin'))


@app.route("/invitation")
def invitation():
    name = session.get('username')
    if name:
        invite = find_invite_for_user(name)
        return render_template("invites.html", invites=invite)
    else:
        return redirect(url_for('loggin'))


@app.route("/invitation/<string:user_name>/<string:respond>")
def result_of_invite(user_name, respond):
    name = session.get('username')
    if name:
        user_id = find_users_id(name)
        if respond == "true":
            respond = True
        else:
            respond = False
        respond_to_invite(name, user_name, user_id, respond)
        return redirect(url_for('all_friends'))
    else:
        return redirect(url_for('loggin'))


@app.route("/find_on_map_f", methods=("GET", "POST"))
def find_on_map_f():
    name = session.get('username')
    # user_d = get_user_info(name)
    if request.method == "POST":
        data = request.get_json()
        lat = float(data.get("lat"))
        lng = float(data.get("lng"))
        print("SAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print(lat, lng, sep="  ,")
        # Фільтруємо пости за отриманими координатами
        global friends2
        ss = get_friends_on_map(lat, lng, name)
        # print(ss, 12, sep=" 232323 ")
        friends2 = get_friends_on_map(lat, lng, name)
        print(friends2)

        # return render_template("place.html", places=res2, name_us=name)

    return render_template("find-on-map_f.html")


@app.route("/friends_on_map", methods=("GET", "POST"))
def friends_on_map():
    name = session.get('username')
    if name:
        return render_template("friends_on_map.html", users=friends2)

    redirect(url_for('loggin'))

# 333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333


@app.route("/send_message_to_dev", methods=("GET", "POST"))
def send_message_to_dev():
    name = session.get('username')
    if request.method == "POST":
        status = request.form["status"]
        message = request.form["message"]
        send_message_on_email(status, message)
        messages_to_dev_default(status)
        return redirect(url_for("user_profile"))
    if name:
        return render_template("send_letter.html")
    else:
        return redirect(url_for('loggin'))


# @app.route("/read_message")
# def read_message():
#     name = session.get('username')
#     if name:
#         letters = []
#         user_id = find_users_id(name)
#         user_data = get_all_message_with_user(user_id)
#         if "letters" in user_data:
#             letters = user_data["letters"]
#         return render_template("letters.html", letters=letters, name_us=name)
#     else:
#         return redirect(url_for('loggin'))


# @app.route("/delete_message/<string:letter_id>")
# def delete_message(letter_id):
#     name = session.get('username')
#     if name:
#         delete_letters(letter_id)
#         return redirect(url_for('read_message'))
#     redirect(url_for('loggin'))


# @app.route("/sort_messages", methods=("GET", "POST"))
# def sort_messages():
#     name = session.get('username')
#     if request.method == "POST":
#         user_id = find_users_id(name)
#         status = request.form["status"]
#         result = sort_letters(user_id, status)
#         return render_template("letters.html", letters=result, name_us=name)
#     if name:
#         return redirect(url_for('read_message'))
#     else:
#         return redirect(url_for('loggin'))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
