import codecs

from scraping.parsers_kz import *

from scraping.models import Vacancy, City, Language


parsers = ((hh, 'https://hh.kz/search/vacancy?clusters=true&area=177&enable_snippets=true&salary=&st=searchVacancy&text=python'),
           (jooble, 'https://kz.jooble.org/SearchResult?rgns=%D0%9A%D0%B0%D1%80%D0%B0%D0%B3%D0%B0%D0%BD%D0%B4%D0%B0&ukw=python')
           )

city = City.objects.filter(slug='karaganda')
jobs, errors = [], []
for funk, url in parsers:
    j, e = funk(url)
    jobs += j
    errors += e

h = codecs.open('work_kz.txt', 'w', 'utf-8')      # Создаём html файл и открываем его в режиме записи, подключая кодек в utf-8 (на всякий случай, если на сайте указана другая кодировка)
h.write(str(jobs))      # Записываем в файл полученную страницу, предварительно преобразовав всё в строку
h.close()       # Закрываем файл

