import codecs
import os, sys      #Для запуска файла вне Django
from scraping.parsers import *


proj = os.path.dirname(os.path.abspath('manage.py'))   #Для запуска файла вне Django. Узнаём абсолютный путь до файла
sys.path.append(proj)   #Для запуска файла вне Django
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"  #Для запуска файла вне Django

import django   #Для запуска файла вне Django
django.setup()  #Для запуска файла вне Django. Сам запуск Django

from django.db import DatabaseError
from scraping.models import Vacancy, City, Language     # Обращаться к файлам проекта нужно после запуска Django


parsers = ((work, 'https://www.work.ua/ru/jobs-kyiv-python/'),
           (rabota, 'https://rabota.ua/zapros/python/%D0%BA%D0%B8%D0%B5%D0%B2')
           )

city = City.objects.filter(slug='kiev').first()     # Получаем QuerySet, и first()'ом приводим к инстансу
language = Language.objects.filter(slug='python').first()
jobs, errors = [], []           # Тут установить точку прерывания и запустить в режиме Debug, чтобы проверить работает ли программа, и не запускать процесс скрапинга
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


# h = codecs.open('work.txt', 'w', 'utf-8')      # Создаём html файл и открываем его в режиме записи, подключая кодек в utf-8 (на всякий случай, если на сайте указана другая кодировка)
# h.write(str(jobs))      # Записываем в файл полученную страницу, предварительно преобразовав всё в строку
# h.close()       # Закрываем файл
