from random import randint
import time
import requests
import bs4
from fake_headers import Headers
from tqdm import tqdm
import json
import os
import sys

if __name__ == "__main__":
    HEADERS = Headers(browser="chrome", os="win", headers=True).generate()
    hh_info = []

    for page in range(0, 18):
        URL = f'https://spb.hh.ru/search/vacancy?search_field=name&text=python+%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE' \
              f'%D1%82%D1%87%D0%B8%D0%BA&from=suggest_post&page={page}&hhtmFrom=vacancy_search_list'
        response = requests.get(URL, headers=HEADERS)
        soup = bs4.BeautifulSoup(response.text, features='html.parser')
        vacancies_on_page = soup.find_all(class_='vacancy-serp-item__layout')
        to_print = f'Парсинг {page} страницы'
        for vacancy in tqdm(vacancies_on_page, desc=to_print):
            title = vacancy.find('h3').find('span').text
            link = vacancy.find('h3').find('a').attrs['href']
            vacancy_info = bs4.BeautifulSoup(requests.get(link, headers=HEADERS).text, features='html.parser')
            experience = vacancy_info.find('p').find('span').text
            salary = vacancy_info.find(class_='vacancy-title').find('span').text
            region = vacancy.find(class_='vacancy-serp-item__info').find(attrs={"data-qa":"vacancy-serp__vacancy-address"}).text
            hh_dict = {'title': title, 'experience': experience, 'salary': salary, 'region': region}
            hh_info.append(hh_dict)
            time.sleep(randint(5,10))
        print(f'\r--> Информация с {page} страницы получена!\r')
        time.sleep(randint(5, 10))
    with open(os.path.join(os.path.dirname(sys.argv[0]), 'hh_info.json'), 'w', encoding="utf-8") as file:
        json.dump(hh_info, file, indent=4,ensure_ascii=False)