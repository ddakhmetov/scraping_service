import os, sys

from django.contrib.auth import get_user_model
from scraping.parsers_kz import *


# ----------------------------
# Для запуска файла вне Django

proj = os.path.dirname(os.path.abspath('manage.py'))   #Для запуска файла вне Django. Узнаём абсолютный путь до файла
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"
# Для запуска файла вне Django
# ----------------------------


import django
django.setup()

# ------------------------------------------------------
# Обращаться к файлам проекта нужно после запуска Django

from django.db import DatabaseError
from scraping.models import Vacancy, City, Language, Errors, \
    Url_kz
# Обращаться к файлам проекта нужно после запуска Django
# ------------------------------------------------------


# ------------------------------------------------------
# Возвращаем пользователя
User = get_user_model()     # В Django не импортируют юзеров из admin.py, а используют такую функцию, которая
                            # возвращает пользователя (ВСЕГО ПОЛЬЗОВАТЕЛЯ), который определён в настройках проекта Django (Settings.py ->
                            # AUTH_USER_MODEL = 'accounts.MyUser'(в данном случае он переопределён))
# Возвращаем пользователя
# ------------------------------------------------------


parsers = ((hh, 'https://hh.kz/search/vacancy?clusters=true&area=177&enable_snippets=true&salary=&st=searchVacancy&text=python'),
           (jooble, 'https://kz.jooble.org/SearchResult?rgns=%D0%9A%D0%B0%D1%80%D0%B0%D0%B3%D0%B0%D0%BD%D0%B4%D0%B0&ukw=python')
           )


# ------------------------------------------
# Получение списка пользователей с рассылкой

def get_settings():
    qs = User.objects.filter(send_email=True).values() # Получаем всех пользователей, подписанных на рассылку. values() - Делает из QuerySet список словарей id [{"citi": "id", "language": "id"}]
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst
# Получение списка пользователей с рассылкой
# ------------------------------------------


# ---------------------------------------------------
# Получение всех интересующих урлов с парами город-ЯП

def get_urls(_settings):
    qs = Url_kz.objects.all().values()
    url_dct = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dct[pair]
        urls.append(tmp)
    return urls
# Получение всех интересующих урлов с парами город-ЯП
# ---------------------------------------------------

q = get_settings()
u = get_urls(q)


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

