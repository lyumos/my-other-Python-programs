import requests
import bs4
from fake_headers import Headers
from datetime import datetime

if __name__ == "__main__":
    KEYWORDS = ['Логические игры', 'Конференции', 'Занимательные задачки', 'Научно-популярное', 'Здоровье']
    HEADERS = Headers(browser="chrome", os="win", headers=True).generate()
    URL = 'https://habr.com/ru/all/'

    response = requests.get(URL, headers=HEADERS)
    text = response.text

    soup = bs4.BeautifulSoup(text, features='html.parser')

    articles = soup.find_all('article')

    for article in articles:
        hubs = article.find_all(class_="tm-article-snippet__hubs-item")
        hubs = [hub.text.strip() for hub in hubs]
        for hub in hubs:
            if hub in KEYWORDS:
                title = article.find('h2').find('span').text
                href = article.find('h2').find('a').attrs['href']
                link = 'https://habr.com' + href
                datetime_published = article.find(class_="tm-article-snippet__meta").find_all("span", attrs={
                    'class': 'tm-article-snippet__datetime-published'})
                for element in datetime_published:
                    datetime_ = element.find('time').attrs['title']
                    formatted_datetime = datetime.strptime(datetime_, "%Y-%m-%d, %H:%M").strftime("%d/%m/%Y %H:%M")
                    print(f'{formatted_datetime} - {title} - {link}')