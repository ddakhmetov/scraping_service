import asyncio
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


parsers = ((hh, 'hh'),
           (jooble, 'jooble')
           )


# ------------------------------------------
# Получение списка пользователей с рассылкой

jobs, errors = [], []

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
    url_dct = {(q['city_id'], q['language_id']): q['url_data_kz'] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data_kz'] = url_dct[pair]
        urls.append(tmp)
    return urls

# Получение всех интересующих урлов с парами город-ЯП
# ---------------------------------------------------


async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)   # await - запускает функцию в асинхронном режиме (запускает функцию, ожидает её результат, при этом происходит переключение на другое выполнение)
    jobs.extend(job)
    errors.extend(err)

settings = get_settings()
url_list = get_urls(settings)


# city = City.objects.filter(slug='karaganda').first()
# language = Language.objects.filter(slug='python').first()
# import time
# start = time.time()

# ------------------------
# Procissing асинхронность

loop = asyncio.get_event_loop()     # Создаётся луп задач
tmp_tasks = [(func, data['url_data_kz'][key], data['city'], data['language'])
             for data in url_list
             for func, key in parsers]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])    # tasks - это таски asincio. Команда на
                                                                        # выполнение. Пробегаемся по tmp_tasks, где "f" -
                                                                        # это кортеж (func, data['url_data_kz'], data['city'], data['language']).
                                                                        # loop.create_task - создаёт задачи, а asyncio.wait() - вызывает эти таски на выполнение.

# Procissing асинхронность
# ------------------------

# for data in url_list:
#     for func, key in parsers:
#         url = data['url_data_kz'][key]
#         j, e = func(url, city=data['city'], language=data['language'])
#         jobs += j
#         errors += e
# print(time.time() - start)  # Печатаем время, за которое исполнится эта часть кода

loop.run_until_complete(tasks)  # Запуск на выполнение
loop.close()    # Закрываем loop, чтобы всё закончилось корректно

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    err = Errors(data=errors).save()


# h = codecs.open('work_kz.txt', 'w', 'utf-8')      # Создаём html файл и открываем его в режиме записи, подключая кодек в utf-8 (на всякий случай, если на сайте указана другая кодировка)
# h.write(str(jobs))      # Записываем в файл полученную страницу, предварительно преобразовав всё в строку
# h.close()       # Закрываем файл
