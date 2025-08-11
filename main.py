import tkinter as tk
from tkinter import messagebox
import requests

# === Настройки ===
YANDEX_API_KEY = "ВСТАВЬ_СВОЙ_API_KEY"  # Получи ключ: https://developer.tech.yandex.ru/
PRICE_PER_KM = 28  # руб/км по анализу рынка

def get_coordinates(address):
    url = f"https://geocode-maps.yandex.ru/1.x/?apikey={YANDEX_API_KEY}&geocode={address}&format=json"
    response = requests.get(url).json()
    try:
        pos = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
        lon, lat = pos.split()
        return float(lat), float(lon)
    except:
        return None

def get_distance_km(start_coords, end_coords):
    url = f"https://api.routing.yandex.net/v2/route?apikey={YANDEX_API_KEY}&waypoints={start_coords[0]},{start_coords[1]}|{end_coords[0]},{end_coords[1]}"
    response = requests.get(url).json()
    try:
        distance_meters = response["routes"][0]["legs"][0]["distance"]["value"]
        return distance_meters / 1000
    except:
        return None

def calculate_price():
    start_address = entry_from.get()
    end_address = entry_to.get()

    if not start_address or not end_address:
        messagebox.showerror("Ошибка", "Введите оба адреса")
        return

    start_coords = get_coordinates(start_address)
    end_coords = get_coordinates(end_address)

    if not start_coords or not end_coords:
        messagebox.showerror("Ошибка", "Не удалось определить координаты. Проверьте адреса.")
        return

    distance_km = get_distance_km(start_coords, end_coords)

    if distance_km is None:
        messagebox.showerror("Ошибка", "Не удалось рассчитать маршрут.")
        return

    price = distance_km * PRICE_PER_KM
    result_label.config(text=f"Расстояние: {distance_km:.1f} км\nСтоимость: {price:.0f} руб.")

root = tk.Tk()
root.title("Калькулятор грузоперевозок Сочи")
root.geometry("400x300")

tk.Label(root, text="Адрес отправления:").pack(pady=5)
entry_from = tk.Entry(root, width=40)
entry_from.pack()

tk.Label(root, text="Адрес назначения:").pack(pady=5)
entry_to = tk.Entry(root, width=40)
entry_to.pack()

tk.Button(root, text="Рассчитать", command=calculate_price).pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

root.mainloop()
