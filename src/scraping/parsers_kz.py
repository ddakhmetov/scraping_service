# Представляемся для сервера браузером
# Делаем запрос на сайт
# Данные поступают в виде краказябр, так как нет кодеков. Преобразуем данные в читабельный вид (на всякий случай)
# Записываем ответ в файл

import requests     # импорт библиотеки для получения данных
import codecs       # импорт библиотеки для преобразования краказябр в текст
from bs4 import BeautifulSoup as BS     # Подключение библиотеки Beautifulsoup
from random import randint


__all__ = ('hh', 'jooble')

headers = [{'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/54.0.2840.99 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*,q=0.8'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/54.0.2840.99 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*,q=0.8'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/54.0.2840.99 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*,q=0.8'},
           {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) '
                          'Version/10.0.1 Safari/602.2.14',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*,q=0.8'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/54.0.2840.71 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*,q=0.8'},
           {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/54.0.2840.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*,q=0.8'},
           {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/54.0.2840.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*,q=0.8'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/54.0.2840.71 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*,q=0.8'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/54.0.2840.99 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*,q=0.8'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*,q=0.8'},
           ]    # Косим под браузер, чтоб сервер нас не завернул


def hh(url, city=None, language=None):
    jobs = []   # Создаём список, куда будут сохраняться словари из цикла for
    errors = []
    if url:
        resp = requests.get(url, headers=headers[randint(0, 9)])  # Отправляем запрос на страницу библиотекой requests
        if resp.status_code == 200:     # Уже используем BS. Проверяем статус. status_code == 200 - получен некий ответ (без ошибок)
            soup = BS(resp.content, 'html.parser')      # Формируем т.н. суп. Принято (если впервые) использовать soup.
            # Указываем, что используется html парсер (обязательно)
            # Определяем главный div, в котором лежит интересующая информация
            main_table = soup.find('div', attrs={'class': 'vacancy-serp'})   # обращаемся к soup, выбираем метод, указываем что мы ищем (div) и вторым параметром конкретизируем
            if main_table:
                div_lst_hh = main_table.find_all('div', attrs={'class': 'vacancy-serp-item'}) #('div', attrs={'class': 'vacancy-serp-item '})     # Внутри нужного div'а ищем те, которые содержат сами вакансии
                dl = codecs.open('dl_kz.txt', 'w', 'utf-8')
                dl.write(str(div_lst_hh))
                dl.close()
                for info in div_lst_hh:
                    pretitle = info.find('span', attrs={'class': 'g-user-content'})
                    title = pretitle.a
                    href = title['href']
                    precontent = info.find('div', attrs={'class': 'g-user-content'})
                    content = precontent.div.text
                    company = 'hh-шечка'
                    #precompany = info.find('div', atrrs={'class': 'vacancy-serp-item__meta-info-company'})
                    #if precompany:
                        #precompany = 'Найдено!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'

                    jobs.append({'title': title.text, 'url': href, 'description': content, 'company': company, 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'div does not exists'})    # Ловим ошибку, когда структура сайта изменилась, и main_div не найден
                err = codecs.open('errors_kz.txt', 'w', 'utf-8')
                err.write(str(errors))
                err.close()
        else:
            errors.append({'url': url, 'title': 'Page do not response'})   # Ловим ошибку, когда главная ссылка перестаёт работать
            err404 = codecs.open('errors_kz404.txt', 'w', 'utf-8')
            err404.write(str(errors))
            err404.close()

    return jobs, errors


def jooble(url, city=None, language=None):
    domain = 'https://kz.jooble.org'
    jobs = []  # Создаём список, куда будут сохраняться словари из цикла for
    errors = []
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])  # Отправляем запрос на страницу библиотекой requests
        if resp.status_code == 200:  # Уже используем BS. Проверяем статус. status_code == 200 - получен некий ответ (без ошибок)
            soup = BS(resp.content, 'html.parser')  # Формируем т.н. суп. Принято (если впервые) использовать soup.
            # Указываем, что используется html парсер (обязательно)
            # Определяем главный div, в котором лежит интересующая информация

    #               ______________________________
    #               |Разбор супа на составляющие |
    #               --------------------------------------------------------------
            main_div = soup.find('div', attrs={'class': '_70404'})  # обращаемся к soup, выбираем метод, указываем что мы ищем (div) и вторым параметром конкретизируем
            if main_div:
                div_lst = main_div.find_all('article', attrs={'class': '_31572 _07ebc'})  # Внутри нужного div'а ищем те, которые содержат сами вакансии
                for div in div_lst:
                    pretitle = div.find('a', attrs={'class': 'baa11'})
                    title = pretitle.span.span.span.text
                    href = pretitle['href']
                    content = div.find('div', attrs={'_0b1c1'})
                    company = div.find('div', attrs={'class', 'caption _8d375'})
    #               Разбор супа на составляющие
    #               ---------------------------------------------------------------

                    jobs.append({'title': title, 'url': domain + href, 'description': content.text, 'company': company.text, 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url,
                               'title': 'div does not exists'})  # Ловим ошибку, когда структура сайта изменилась, и main_div не найден
        else:
            errors.append(
                {'url': url, 'title': 'Page do not response'})  # Ловим ошибку, когда главная ссылка перестаёт работать

    return jobs, errors


#if __name__ == '__main__':
#    url = 'url'
#    jobs, errors = hh(url)
#    h = codecs.open('work_kz.txt', 'w', 'utf-8')      # Создаём html файл и открываем его в режиме записи, подключая кодек в utf-8 (на всякий случай, если на сайте указана другая кодировка)
#    h.write(str(jobs))      # Записываем в файл полученную страницу, предварительно преобразовав всё в строку
#    h.close()       # Закрываем файл

#                   -----Получение данных-----


