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

        req = requests.get(url="https://telemarket24.ru/catalog/telefony_i_smartfony/", headers=headers)
        src = req.text

        with open(f"data/{count}_{category_name}.html", "w", encoding="utf-8") as file:
            file.write(src)

        count += 1