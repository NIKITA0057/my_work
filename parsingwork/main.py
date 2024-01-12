import requests
from bs4 import BeautifulSoup
import lxml
import csv

#

# page_with_item = requests.get(urls_list[0])

# with open('page.html', 'r') as f:
#     page = f.read()
#     pg = BeautifulSoup(page, 'lxml')
#
# print(itm)


def check_count(url='https://rzkk.net/catalog/montazhnye-sistemy/'):
    count = requests.get(url).text
    list_count = []
    pg = BeautifulSoup(count, 'lxml')
    counter = pg.find('div', class_='counter').find_all('a')
    for i in counter:
        if i.text:
            list_count.append('https://rzkk.net' + i.get('href'))
    return list_count


def serch_url_card(url):
    info_serch = requests.get(url).text
    sop = BeautifulSoup(info_serch, 'lxml')
    url = sop.find_all('a', class_='cat_list_name')
    itm = []
    for i in url:
        itm.append('https://rzkk.net' + i.get('href'))
    return itm


def check_first_card():
    responce = requests.get('https://rzkk.net/catalog/').text

    soup = BeautifulSoup(responce, 'lxml')

    urls_list = []
    a = soup.find_all('a', class_='prod_list_img')
    for i in a:
        urls_list.append('https://rzkk.net' + i.get('href'))
    return urls_list


def get_info(url='https://rzkk.net/catalog/montazhnye-sistemy/skoba-k1157.html'):
    types_l = []
    weight_l = []
    sizea_l = []
    metal_thicks_l = []
    metal_thicks_p_l = []
    height_l = []
    lengh_l = []
    number_holes_l = []
    max_load_l = []
    hfirs_l = []
    withb_l = []
    withbfirst_l = []
    count_info_l = []

    inf = requests.get(url).text
    soup = BeautifulSoup(inf, 'lxml')
    name = soup.find('meta', {'name': 'keywords'}).get('content')
    count_info = soup.find_all('input', {'type': 'checkbox'})
    for i in count_info:
        count_info_l.append(i.get('value'))
    bfirst = soup.find_all('div', {'class': 'row-item', 'data-code': 'WIDTH_B1'})
    if bfirst:
        for i in bfirst:
            withbfirst_l.append(i.get('data-val'))

    b = soup.find_all('div', {'class': 'row-item', 'data-code': 'WIDTH_B'})
    if b:
        for i in b:
            withb_l.append(i.get('data-val'))


    hfirst = soup.find_all('div', {'class': 'row-item', 'data-code': 'SIZE__H1'})
    if hfirst:
        for i in hfirst:
            hfirs_l.append(i.get('data-val'))
    types = soup.find_all('div', {'class': 'row-item', 'data-code': 'TYPE'})
    if types:
        for i in types:
            types_l.append(i.get('data-val'))
    weight = soup.find_all('div', {'class': 'row-item', 'data-code': 'WEIGHT'})
    if weight:
        for i in weight:
            weight_l.append(i.get('data-val') + 'kg')
    # metal_thick = soup.find_all('div', {'class': 'row-item', 'data-code': 'METAL_THICKNESS'})
    # if metal_thick:
    #     for i in metal_thick:
    #         methal_tihck_l.append(i.get('data-val'))
    size_a = soup.find_all('div', {'class': 'row-item', 'data-code': 'SIZE_A'})
    if size_a:
        for i in size_a:
            sizea_l.append(i.get('data-val'))
    metal_thicks = soup.find_all('div', {'class': 'row-item', 'data-code': 'METAL_THICKNESS_S'})
    if metal_thicks:
        for i in metal_thicks:
            metal_thicks_l.append(i.get('data-val'))
    metal_thicks_p = soup.find_all('div', {'class': 'row-item', 'data-code': 'METAL_THICKNESS_P'})
    if metal_thicks_p:
        for i in metal_thicks_p:
            metal_thicks_p_l.append(i.get('data-val'))
    height = soup.find_all('div', {'class': 'row-item', 'data-code': 'HEIGHT'})
    if height:
        for i in height:
            height_l.append(i.get('data-val'))
    lenght = soup.find_all('div', {'class': 'row-item', 'data-code': 'LENGTH'})
    if lenght:
        for i in lenght:
            lengh_l.append(i.get('data-val'))
    number_holes = soup.find_all('div', {'class': 'row-item', 'data-code': 'NUMBER_HOLES'})
    if number_holes:
        for i in number_holes:
            number_holes_l.append(i.get('data-val'))
    max_load = soup.find_all('div', {'class': 'row-item', 'data-code': 'MAX_LOAD'})
    if max_load:
        for i in max_load:
            max_load_l.append(i.get('data-val'))

    final_document = {}
    for i in range(len(count_info_l)):
        final_document[name] = {

            'B':withb_l[i] if i < len(withb_l) else None,
            'B1':withbfirst_l[i] if i < len(withbfirst_l) else None,
            'H1 mm': hfirs_l[i] if i < len(hfirs_l) else None,
            'тип': types_l[i] if i < len(types_l) else None,
            'A': sizea_l[i] if i < len(sizea_l) else None,
            'Толщина металла стойки': metal_thicks_l[i] if i < len(metal_thicks_l) else None,
            "Толщина металла полки": metal_thicks_p_l[i] if i < len(metal_thicks_p_l) else None,
            'Высота H (мм.)': height_l[i] if i < len(height_l) else None,
            'Длина L (мм.)': lengh_l[i] if i < len(lengh_l) else None,
            'Вес изделия (кг.)': weight_l[i] if i < len(weight_l) else None,
            'Количество отверстий (шт.)': number_holes_l[i] if i < len(number_holes_l) else None,
            'Макс. нагрузка (кг.)': max_load_l[i] if i < len(max_load_l) else None,

        }

        csv_file_path = 'монтажные системы.csv'
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'тип', 'A', 'Толщина металла стойки', 'Толщина металла полки', 'Высота H (мм.)',
                          'Длина L (мм.)',
                          'Вес изделия (кг.)', 'Количество отверстий (шт.)', 'Макс. нагрузка (кг.)',
                          'Толщина металла стойки']

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Записываем заголовки
            writer.writeheader()






#
def main():
    for i in range(1):
        a = check_first_card()
        b = serch_url_card(a[i])
        c = check_count(a[i])
        for x in b:
            get_info(x)
        if c:
            for i in c:
                list_pag = serch_url_card(i)
            for x in list_pag:
                get_info(x)


main()
