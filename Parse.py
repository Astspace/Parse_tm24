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
#
# with open("index.html", "w", encoding="utf-8") as file:
#    file.write(src)

with open("index.html", encoding="utf-8") as file:
    src = file.read()

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
    rep = [",", " ", "-"]
    for char in rep:
        if char in category_name:
            category_name = category_name.replace(char, "_")

    req = requests.get(url=category_href, headers=headers)
    req.encoding = "utf-8"
    src = req.text

    if not os.path.exists(f"data/{count}_{category_name}"):
        os.mkdir(f"data/{count}_{category_name}")

    soup = BeautifulSoup(src, "lxml")

    all_subcategories_data = soup.find_all(class_="catalog-menu-lvl0-item no-numbers")[count].find_all(class_="catalog-menu-lvl1")
    count_sub = 0
    for subcategory_data in all_subcategories_data:
        #if count_sub == 0:
        subcategory_name = subcategory_data.find(class_="menu-lvl1-link").text.strip()
        subcategory_link = "https://telemarket24.ru" + subcategory_data.find(class_="menu-lvl1-link").get("href")
        count_item = 0

        excel_file = Workbook()
        excel_sheet = excel_file.active

        excel_sheet["A1"] = "Наименование товара"
        excel_sheet["B1"] = "Наличие товара, ед."
        excel_sheet["C1"] = "Стоимость товара,руб."
        excel_sheet["D1"] = "Ссылка на товар"

        print(f"--- ЗАПОЛНЯЕМ ФАЙЛ {category_name}/{subcategory_name}--- \nЗаголовки добавлены.")
        if subcategory_data.ul != None:
            item_data = subcategory_data.ul.find_all("a")
            len_item = len(item_data)
            for item in item_data:
                item_name = item.text.strip()
                item_link = "https://telemarket24.ru" + item.get("href")

                req = requests.get(item_link, headers=headers)
                req.encoding = "utf-8"
                src = req.text

                # with open(f"data/{count}_{category_name}/{item_name}.html", "w", encoding="utf-8") as file:
                #     file.write(src)
                #
                # with open(f"data/{count}_{category_name}/{item_name}.html", encoding="utf-8") as file:
                #     src = file.read()

                excel_sheet.append([item_name])
                print(f"++ Категория (заголовок) {item_name} раздела {subcategory_name} добавлена.")

                soup = BeautifulSoup(src, "lxml")

                all_products = soup.find_all(class_="main-data")
                count_product = 0
                len_products = len(all_products)
                for product in all_products:
                    product_name = product.find(class_="name").text.strip()
                    if product.find(class_="info-tag tovar_availability") != None:
                        product_availability = product.find(class_="info-tag tovar_availability").find("span").text.strip()
                    else:
                        product_availability = "Нет в наличии"
                    product_price = product.find(class_="price").find(class_="value").text.strip()
                    product_link = "https://telemarket24.ru" + product.find(class_="name").find("a").get("href")

                    excel_sheet.append([product_name, product_availability, product_price, product_link])
                    print(f"     Добавлен товар: || {product_name}")
                    excel_file.save(filename=f"data/{count}_{category_name}/{subcategory_name}.xlsx")
                    count_product += 1
                count_item += 1
                if count_item == len_item and count_product == len_products:
                    print(f"*** ФАЙЛ {category_name}/{subcategory_name} CОХРАНЕН ***")
        else:
            req = requests.get(url=subcategory_link, headers=headers)
            req.encoding = "utf-8"
            src = req.text
            soup = BeautifulSoup(src, "lxml")
            all_products = soup.find_all(class_="main-data")
            count_product = 0
            len_products = len(all_products)
            for product in all_products:
                product_name = product.find(class_="name").text.strip()
                product_availability = product.find(class_="info-tag tovar_availability").find("span").text.strip()
                product_price = product.find(class_="price").find(class_="value").text.strip()
                product_link = "https://telemarket24.ru" + product.find(class_="name").find("a").get("href")

                excel_sheet.append([product_name, product_availability, product_price, product_link])
                print(f"     Добавлен товар: || {product_name}")
                excel_file.save(filename=f"data/{count}_{category_name}/{subcategory_name}.xlsx")
                count_product += 1
            if count_product == len_products:
                print(f"*** ФАЙЛ {category_name}/{subcategory_name} CОХРАНЕН ***")

        count_sub += 1
    count += 1
    print(f"----------\nВСЕ ФАЙЛЫ КАТЕГОРИИ {category_name} СОХРАНЕНЫ!\n----------\n\n")
print("РАБОТА ПРОГРАММЫ ЗАКОНЧЕНА!")