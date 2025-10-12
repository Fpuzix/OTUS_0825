import json

from csv import DictReader
from files import CSV_FILE_PATH
from files import JSON_FILE_PATH


# Создание списка пользователей
with open(JSON_FILE_PATH, "r") as f:
    users = json.load(f)
    user_list = []

    for u in users:
        # безопасно вытаскиваем поля (если каких-то нет — подставим пустое)
        user_list.append(
            {
                "name": u.get("name", ""),
                "gender": u.get("gender", ""),
                "address": u.get("address", ""),
                "age": u.get("age", ""),
                "books": [],
            }
        )


# Создание списка книг
with open(CSV_FILE_PATH, newline="") as f:
    reader = DictReader(f)
    books_list = []

    for b in reader:
        books_list.append(
            {
                "title": b["Title"],
                "author": b["Author"],
                "pages": int(b["Pages"]),
                "genre": b["Genre"],
            }
        )


# Цикл для соединения двух списков
i, j = 0, 0
while i < len(books_list):
    if j < len(user_list):
        user_list[j]["books"].append(books_list[i])
        j += 1
    else:
        j = 0
    i += 1


# Записываем в файл
with open("result.json", "w") as f:
    json.dump(user_list, f, indent=4)
