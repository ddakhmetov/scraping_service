import codecs
import os, sys
from scraping.parsers_kz import *


proj = os.path.dirname(os.path.abspath('manage.py'))   #Для запуска файла вне Django. Узнаём абсолютный путь до файла
sys.path.append(proj)   #Для запуска файла вне Django
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"  #Для запуска файла вне Django

import django
django.setup()

from django.db import DatabaseError
from scraping.models import Vacancy, City, Language, Errors     # Обращаться к файлам проекта нужно после запуска Django


parsers = ((hh, 'https://hh.kz/search/vacancy?clusters=true&area=177&enable_snippets=true&salary=&st=searchVacancy&text=python'),
           (jooble, 'https://kz.jooble.org/SearchResult?rgns=%D0%9A%D0%B0%D1%80%D0%B0%D0%B3%D0%B0%D0%BD%D0%B4%D0%B0&ukw=python')
           )

city = City.objects.filter(slug='karaganda').first()
language = Language.objects.filter(slug='python').first()
jobs, errors = [], []
for funk, url in parsers:
    j, e = funk(url)
    jobs += j
    errors += e


for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    err = Errors(data=errors).save()


# h = codecs.open('work_kz.txt', 'w', 'utf-8')      # Создаём html файл и открываем его в режиме записи, подключая кодек в utf-8 (на всякий случай, если на сайте указана другая кодировка)
# h.write(str(jobs))      # Записываем в файл полученную страницу, предварительно преобразовав всё в строку
# h.close()       # Закрываем файл

