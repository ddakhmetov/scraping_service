import requests
import codecs

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml;q=0.9,*/*,q=0.8'
           }    # Косим под браузер, чтоб сервер нас не завернул

url = 'https://hh.kz/search/vacancy?clusters=true&area=177&enable_snippets=true&salary=&st=searchVacancy&text=python'    # Указываем url страницы, которую будем получать
resp = requests.get(url, headers=headers)           # Отправляем запрос на страницу библиотекой requests

h = codecs.open('work_kz.html', 'w', 'utf-8')      # Создаём html файл и открываем его в режиме записи, подключая кодек в utf-8 (на всякий случай, если на сайте указана другая кодировка)
h.write(str(resp.text))      # Записываем в файл полученную страницу, предварительно преобразовав всё в строку
h.close()       # Закрываем файл
