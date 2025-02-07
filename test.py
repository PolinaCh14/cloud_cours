import folium
import math


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


def find_points_in_radius(target_lat, target_lon, radius, points):
    """
    Знаходить всі точки, що знаходяться в заданому радіусі від заданої точки.

    Параметри:
    target_lat, target_lon: float, широта та довгота заданої точки в градусах
    radius: float, радіус в кілометрах
    points: list of tuples, список кортежів (lat, lon), координати інших точок

    Повертає:
    list of tuples, список координат точок, які знаходяться в заданому радіусі
    """
    points_in_radius = []
    for point in points:
        # Обчислення відстані між заданою точкою та поточною точкою з бази даних
        distance = haversine_distance(
            target_lat, target_lon, point[0], point[1])
        # Перевірка, чи відстань менше заданого радіусу
        if distance <= radius:
            points_in_radius.append(point)
    return points_in_radius


# Приклад використання
target_lat = 52.2296756
target_lon = 21.0122287
radius = 5000  # радіус у кілометрах

# Припустимо, що у нас є список точок у форматі (lat, lon)
points = [
    (50.856614, 20.3522219),  # Париж
    (40.712776, -74.005974),  # Нью-Йорк
    (51.507351, -0.127758),  # Лондон
    # Додайте інші точки, які вам потрібно перевірити
]

# Знаходимо всі точки, які знаходяться в радіусі 100 кілометрів від заданої точки
points_in_radius = find_points_in_radius(
    target_lat, target_lon, radius, points)

# Виводимо результат
print("Точки, які знаходяться в радіусі", radius, "км від заданої точки:")
for point in points_in_radius:
    print("Координати:", point)
