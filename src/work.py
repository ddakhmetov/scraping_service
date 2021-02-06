# Представляемся для сервера браузером
# Делаем запрос на сайт
# Данные поступают в виде краказябр, так как нет кодеков. Преобразуем данные в читабельный вид (на всякий случай)
# Записываем ответ в файл

import requests     # импорт библиотеки для получения данных
import codecs       # импорт библиотеки для преобразования краказябр в текст
from bs4 import BeautifulSoup as BS     # Подключение библиотеки Beautifulsoup


#                   -----Получение данных-----

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml;q=0.9,*/*,q=0.8'
           }    # Косим под браузер, чтоб сервер нас не завернул





def work(url):

    jobs = []  # Создаём список, куда будут сохраняться словари из цикла for
    errors = []
    domain = 'https://www.work.ua'
    url = 'https://www.work.ua/ru/jobs-kyiv-python/'    # Указываем url страницы, которую будем получать
    resp = requests.get(url, headers=headers)           # Отправляем запрос на страницу библиотекой requests
    if resp.status_code == 200:     # Уже используем BS. Проверяем статус. status_code == 200 - получен некий ответ (без ошибок)
        soup = BS(resp.content, 'html.parser')      # Формируем т.н. суп. Принято (если впервые) использовать soup.
        # Указываем, что используется html парсер (обязательно)
        # Определяем главный div, в котором лежит интересующая информация
        main_div = soup.find('div', id='pjax-job-list')   # обращаемся к soup, выбираем метод, указываем что мы ищем (div) и вторым параметром конкретизируем
        if main_div:
            div_lst = main_div.find_all('div', attrs={'class': 'job-link'})     #Внутри нужного div'а ищем те, которые содержат сами вакансии
            for div in div_lst:
                tittle = div.find('h2')
                href = tittle.a['href']
                content = div.p.text
                company = 'No name'
                logo = div.find('img')
                if logo:
                    company = logo['alt']
                jobs.append({'tittle': tittle.text, 'url': domain + href, 'description': content, 'company': company})
        else:
            errors.append({'url': url, 'tittle': 'div does not exists'})    # Ловим ошибку, когда структура сайта изменилась, и main_div не найден
    else:
        errors.append({'url': url, 'tittle': 'Page do not response'})   # Ловим ошибку, когда главная ссылка перестаёт работать

    return jobs, errors


def rabota(url):

    jobs = []  # Создаём список, куда будут сохраняться словари из цикла for
    errors = []
    domain = 'https://rabota.ua'
    resp = requests.get(url, headers=headers)           # Отправляем запрос на страницу библиотекой requests
    if resp.status_code == 200:     # Уже используем BS. Проверяем статус. status_code == 200 - получен некий ответ (без ошибок)
        soup = BS(resp.content, 'html.parser')      # Формируем т.н. суп. Принято (если впервые) использовать soup.
        # Указываем, что используется html парсер (обязательно)
        # Определяем главный div, в котором лежит интересующая информация
        table = soup.find('table', id='ctl00_content_vacancyList_gridList')   # обращаемся к soup, выбираем метод, указываем что мы ищем (div) и вторым параметром конкретизируем
        if table:
            tr_lst = table.find_all('tr', attrs={'id': True})     #Внутри нужного div'а ищем те, которые содержат сами вакансии
            for tr in tr_lst:
                div = tr.find('div', attrs={'class': 'card-body'})
                if div:
                    tittle = div.find('h2', attrs={'class': 'card-title'})
                    href = tittle.a['href']
                    content = div.find('div', attrs={'class': 'card-description'})
                    company = 'No name'
                    co = div.find('p', attrs={'class', 'company-name'})
                    if co:
                        company = co.a.text
                jobs.append({'tittle': tittle.text, 'url': domain + href, 'description': content.text, 'company': company})
        else:
            errors.append({'url': url, 'tittle': 'Table does not exists'})    # Ловим ошибку, когда структура сайта изменилась, и main_div не найден
    else:
        errors.append({'url': url, 'tittle': 'Page do not response'})   # Ловим ошибку, когда главная ссылка перестаёт работать

    return jobs, errors


if __name__ == '__main__':
    url = 'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2'
    jobs, errors = rabota(url)
    h = codecs.open('work.txt', 'w', 'utf-8')      # Создаём html файл и открываем его в режиме записи, подключая кодек в utf-8 (на всякий случай, если на сайте указана другая кодировка)
    h.write(str(jobs))      # Записываем в файл полученную страницу, предварительно преобразовав всё в строку
    h.close()       # Закрываем файл

#                   -----Получение данных-----


