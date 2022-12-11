from collections import deque
import requests
import sqlite3
from bs4 import BeautifulSoup

MainURL = "https://ria.ru"  # корневой каталог

ALL_URL = set()  # все сылки на сайте
DB_connect = sqlite3.connect("SQL/DataSet.db")

Deque_URL = deque()  # очередь еще не проверенных ссылок
Deque_URL.append(MainURL)

MAX_Stack = 770


def GetArrayUrl(CurentUrl):
    html_text = requests.get(CurentUrl).text
    soup = BeautifulSoup(html_text, 'html.parser')
    URL_Array = soup.findAll('a')
    for element in URL_Array:
        URL: str = element.get('href')
        if URL is not None:
            if URL.startswith("https://ria.ru"):
                if URL not in ALL_URL:
                    print(URL)
                    ALL_URL.add(URL)
                    Deque_URL.append(URL)
            '''       
            elif URL.startswith("/") and 'search' not in URL:
                if CurentUrl + URL not in ALL_URL:
                    print(CurentUrl + URL)
                    ALL_URL.add(CurentUrl + URL)
                    Deque_URL.append(CurentUrl + URL)
            '''


def StartParsURL():
    count: int = 0
    while count < MAX_Stack and len(Deque_URL) != 0:
        count += 1
        print(count)
        _url = Deque_URL.pop()
        DeqCount: str = str(len(Deque_URL))
        print('Посещаем - ' + _url + " Deque - " + DeqCount + " Уникальных ссылок - " + str(len(ALL_URL)))
        GetArrayUrl(_url)

    i = 0
    for Url in ALL_URL:
        print(str(i) + "   " + Url)
        i += 1
        ReturnContent(Url, i)


def ReturnContent(url, filename):
    if url is not None:
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        Date_ARR = soup.find("div", "article__info-date")
        Article = soup.find("h1", "article__title")
        texts = ''
        texts_Arr = soup.find_all("div", "article__text")

        if texts_Arr is not None:
            for t in texts_Arr:
                texts += t.text
    if (Date_ARR is not None):
        print('NotDay')
    if (Article is not None):
        print('NotArticle')
    if (texts is not None):
        print('non text')


    if (Date_ARR is not None) and (Article is not None) and (texts is not None):
        f = open('/Users/ilya/HomeWork/WebScrap/files/' + str(filename) + '.txt', 'w')
        print(Date_ARR.text + "\n" + " " + "\n" + Article.text + "\n" + " " + "\n" + texts)
        f.write(Date_ARR.text + "\n" + Article.text + "\n" + texts)
        f.close()


        # print(Date_ARR, Date_ARR, Article.text, texts)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    StartParsURL()
    #ReturnContent('https://ria.ru/20220803/borsch-1806766968.html#1806766968-10', 1)
