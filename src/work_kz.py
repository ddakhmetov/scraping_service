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


def hh():
    domain = 'https://www.work.ua'
    url = 'https://karaganda.hh.kz/search/vacancy?clusters=true&area=177&enable_snippets=true&salary=&st=searchVacancy&text=python&customDomain=1'    # Указываем url страницы, которую будем получать
    resp = requests.get(url, headers=headers)           # Отправляем запрос на страницу библиотекой requests
    jobs = []   # Создаём список, куда будут сохраняться словари из цикла for
    errors = []
    if resp.status_code == 200:     # Уже используем BS. Проверяем статус. status_code == 200 - получен некий ответ (без ошибок)
        soup = BS(resp.content, 'html.parser')      # Формируем т.н. суп. Принято (если впервые) использовать soup.
        # Указываем, что используется html парсер (обязательно)
        # Определяем главный div, в котором лежит интересующая информация
        main_div = soup.find('div', attrs={'class': 'vacancy-serp'})   # обращаемся к soup, выбираем метод, указываем что мы ищем (div) и вторым параметром конкретизируем
        if main_div:
            div_lst = main_div.find_all('div', attrs={'class': 'vacancy-serp-item'})     # Внутри нужного div'а ищем те, которые содержат сами вакансии
            for div in div_lst:
                tittle = div.find('a', attrs={'class': 'bloko-link'})
                href = tittle['href']
                precontent = div.find('div', attrs={'g-user-content'})
                content = precontent.div.text
                company = div.find('a', attrs={'class', 'bloko-link_secondary'})

                jobs.append({'tittle': tittle.text, 'url': href, 'description': content, 'company': company.text})
        else:
            errors.append({'url': url, 'tittle': 'div does not exists'})    # Ловим ошибку, когда структура сайта изменилась, и main_div не найден
    else:
        errors.append({'url': url, 'tittle': 'Page do not response'})   # Ловим ошибку, когда главная ссылка перестаёт работать

    return jobs, errors


def jooble(url):
    domain = 'https://kz.jooble.org'
    resp = requests.get(url, headers=headers)  # Отправляем запрос на страницу библиотекой requests
    jobs = []  # Создаём список, куда будут сохраняться словари из цикла for
    errors = []
    if resp.status_code == 200:  # Уже используем BS. Проверяем статус. status_code == 200 - получен некий ответ (без ошибок)
        soup = BS(resp.content, 'html.parser')  # Формируем т.н. суп. Принято (если впервые) использовать soup.
        # Указываем, что используется html парсер (обязательно)
        # Определяем главный div, в котором лежит интересующая информация
        main_div = soup.find('div', attrs={'class': '_70404'})  # обращаемся к soup, выбираем метод, указываем что мы ищем (div) и вторым параметром конкретизируем
        if main_div:
            div_lst = main_div.find_all('article', attrs={'class': '_31572 _07ebc'})  # Внутри нужного div'а ищем те, которые содержат сами вакансии
            for div in div_lst:
                pretitle = div.find('a', attrs={'class': 'baa11'})
                title = pretitle.span.span.span.text
                href = pretitle['href']
                content = div.find('div', attrs={'_0b1c1'})
                company = div.find('div', attrs={'class', 'caption _8d375'})

                jobs.append({'tittle': title, 'url': domain + href, 'description': content.text, 'company': company.text})
        else:
            errors.append({'url': url,
                           'title': 'div does not exists'})  # Ловим ошибку, когда структура сайта изменилась, и main_div не найден
    else:
        errors.append(
            {'url': url, 'tittle': 'Page do not response'})  # Ловим ошибку, когда главная ссылка перестаёт работать

    return jobs, errors


if __name__ == '__main__':
    url = 'https://kz.jooble.org/SearchResult?rgns=%D0%9A%D0%B0%D1%80%D0%B0%D0%B3%D0%B0%D0%BD%D0%B4%D0%B0&ukw=python'
    jobs, errors = jooble(url)
    h = codecs.open('work_kz.txt', 'w', 'utf-8')      # Создаём html файл и открываем его в режиме записи, подключая кодек в utf-8 (на всякий случай, если на сайте указана другая кодировка)
    h.write(str(jobs))      # Записываем в файл полученную страницу, предварительно преобразовав всё в строку
    h.close()       # Закрываем файл

#                   -----Получение данных-----


