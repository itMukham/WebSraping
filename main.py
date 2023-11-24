import csv
import datetime
import json
from random import randint

import requests
from bs4 import BeautifulSoup


#функция отправки запроса на url
def url(url):
    respons = requests.get(url)

    return respons

#функция обработки результата ответа с предыдущей
def text(respons):
    #глобальные переменные
    global fair, good, flawless
    data = []
    carriers = [["/at-t"," AT$T"] , ["/t-mobile", " T-MOBLE"]] #, ["/sprint", " SPRINT"], ["/unlocked", " UNLOKED"], ["/verizon"," VERSION"]]
    colors = [["-black", " BLACK"] , ["-green", " GREEN"]]#, ["-purple", " PURPLE"], ["-red", " RED"],["-white", " WHITE"], ["-yellow", " YELLOW"], ["-blue", " BLUE"], ["-grey", " GREY"], ["-gold", " GOLD"], ["-silver", " SILVER"]]
    capacitys = [["-64gb", " 64GB"], ["-128gb", " 128GB"]]#, ["-256gb"," 256GB"], ["-512gb"," 512GB"]]
    conditions = [["perfect", " PERFECT "]]#, ["good", " GOOD "], ["poor", " POOR "]]
    condins = [["%20-%20Turns%20On#offer", " YES "]]#, ["%20-%20Broken#offer", " NO "]]
    broken=0
    fair=0
    good=0
    flawless=0
    #перевод результата в html
    soup = BeautifulSoup(response.content, "html.parser")
    #выборка нужных элементов в массив продуктов
    products = soup.find_all("a", class_="pdp-page-link")
    #перебор массива продуктов
    for product in products:

        name = product.find("h2").text

        # Извлекаем значение 648 из блока HTML
        price_span = product.findAll('span')
        price_value = price_span[1].text
        print(name + " Price - "+ price_value)
       #формирование ссылки на телефон
        href = "https://www.trademore.com" + product.attrs["href"]
        print(href)
        for carrier in carriers:
            href1 = href + carrier[0]
            name1 = name + carrier[1]
            for color in colors:
                href2 = href1 + color[0]
                name2 = name1 + color[1]
                for capasity in capacitys:
                    href3 = href2 + capasity[0]
                    name3 = name2 + capasity[1]

                    name5 = ""
                    i = 0
                    for condition in conditions:

                        if condition[0] != "poor":
                            href4 = href3 + "?condition=" + condition[0]
                            name4 = name3 + condition[1]
                            nname4 = name4 + " PRICE - " + str(int(price_value) + randint(50, 100))
                            print(nname4)
                            resp = url(href4)
                            soup1 = BeautifulSoup(resp.content, "html.parser")
                            pr1 = soup1.find_all("script")


                        else:
                            for condin in condins:
                                href4 = href3 + "?condition=" + condition[0] + condin[0]
                                name4 = name3 + condition[1] + condin[1]
                                print(href4)
                                resp = url(href4)
                                soup1 = BeautifulSoup(resp.content, "html.parser")
                                pr1 = soup1.find_all("script")
                                name5 = ""
                                i = 0
                                for condition in conditions:

                                    if condition[0] != "poor":
                                        href4 = href3 + "?condition=" + condition[0]

                                        name4 = name3 + condition[1]
                                        nname4 = name4 + " PRICE - "+str(int(price_value) + randint(50, 100))

                                        resp = url(href4)
                                        soup1 = BeautifulSoup(resp.content, "html.parser")
                                        #pr1 = soup1.find_all("script")




                    d = {
                        'name': name3,
                        'type': 'iphone',
                        'site': 'trademore.com',
                        'url': href3,
                        'broken': broken,
                        'fair': fair,
                        'good': good,
                        'flawless': flawless,
                        'new': 0,
                        'params': [],
                        'prices': int(price_value) + randint(50, 100),
                    }
                    print(nname4)
                    #print(d)
                    data.append(d)
                # можн а тайм аут

    return data

def document(data):
    with open("parser2.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows([data])
        print("Файл создан")

def docjson(data):
    devices = json.dumps(data)
    with open("devises.json", "w") as my_file:
        my_file.write(devices)

devices = [
    {
        'name': 'Apple iPhone XR T-Mobile 128GB Black',
        'type': 'iphone',
        'site': 'trademore.com',
        'url': 'https://www.trademore.com/sell/iphone/iphone-xr/t-mobile-black-128gb',
        'time': '2023-03-17 20:39:00',
        'broken': 15,
        'fair': 43,
        'good': 77,
        'flawless': 86,
        'new': 0,
        'params': [],
        'prices': [],
    }
]
json_data = json.dumps(devices)

response = url("http://www.trademore.com/sell/iphone/")
data = text(response)
# response = url("https://www.trademore.com/sell/iphone?page=2")
document(data)
docjson(data)