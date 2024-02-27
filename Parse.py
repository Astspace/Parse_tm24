import csv

import requests
from bs4 import BeautifulSoup
import json
import http.client

http.client._MAXHEADERS = 100000

# url = "https://telemarket24.ru/catalog/"
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}
# req = requests.get(url, headers=headers)
# src = req.text

# with open ("index.html", "w", encoding="utf-8") as file:
#    file.write(src)

# with open("index.html", encoding="utf-8") as file:
#     src = file.read()
#
# soup = BeautifulSoup(src, "lxml")
# all_category = soup.find_all(class_="menu-lvl0-link")
# all_category_dict = {}
# for item in all_category:
#     item_text = item.text.strip()
#     item_link = "https://telemarket24.ru" + item.get("href")
#     all_category_dict[item_text] = item_link

# with open("all_category_dict.json", "w") as file:
#     json.dump(all_category_dict, file, indent=4, ensure_ascii=False)

with open("all_category_dict.json") as file:
    all_categories = json.load(file)

count = 0
for category_name, category_href in all_categories.items():
    if count == 0:
        rep = [",", " ", "-"]
        for item in rep:
            if item in category_name:
                category_name = category_name.replace(item, "_")

        # req = requests.get(url=category_href, headers=headers)
        # src = req.text
        #
        # with open(f"data/{count}_{category_name}.html", "w", encoding="utf-8") as file:
        #     file.write(src)

        with open(f"data/{count}_{category_name}.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        product = soup.find(class_="main-data")
        product_name = product.find(class_="name").text.strip()
        product_availability = product.find(class_="info-tag").find("span").text.strip()
        product_price = product.find(class_="price").find(class_="value").text.strip()
        product_link = "https://telemarket24.ru" + product.find(class_="name").find("a").get("href")
        print(product_link)
        print(product)

        with open(f"data/{count}_{category_name}.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    "Наименование товара",
                    "Наличие товара",
                    "Стоимость товара, руб.",
                    "Ссылка на товар"
                )
            )

        count += 1