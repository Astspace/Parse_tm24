import requests
from bs4 import BeautifulSoup
import json
import http.client
from openpyxl import Workbook
import os

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

with open("index.html", encoding="utf-8") as file:
    src = file.read()
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

        if not os.path.exists(f"data/{count}_{category_name}"):
            os.mkdir(f"data/{count}_{category_name}")


        soup = BeautifulSoup(src, "lxml")

        all_subcategories_data = soup.find(class_="catalog-menu-lvl1-wrap").find_all(class_="catalog-menu-lvl1")
        count_subcategoty = 0
        for subcategory_data in all_subcategories_data:
            if count_subcategoty == 0:
                subcategory_name = subcategory_data.find(class_="menu-lvl1-header").find(class_="menu-lvl1-link").find("span").text.strip()
                count_subcategoty += 1
                print(subcategory_name)

        product = soup.find(class_="main-data")
        product_name = product.find(class_="name").text.strip()
        product_availability = product.find(class_="info-tag").find("span").text.strip()
        product_price = product.find(class_="price").find(class_="value").text.strip()
        product_link = "https://telemarket24.ru" + product.find(class_="name").find("a").get("href")

        file = Workbook()
        sheet = file.active
        sheet["A1"] = "Наименование товара"
        sheet["B1"] = "Наличие товара, ед."
        sheet["C1"] = "Стоимость товара,руб."
        sheet["D1"] = "Ссылка на товар"
        # sheet.append([product_name, product_availability, product_price, product_link])
        # file.save(filename=f"data/{count}_{category_name}.xlsx")

        count += 1