import os, sys
from django.contrib.auth import get_user_model
import django
from django.core.mail import EmailMultiAlternatives


# ----------------------------
# Для запуска файла вне Django

proj = os.path.dirname(os.path.abspath('manage.py'))   #Для запуска файла вне Django. Узнаём абсолютный путь до файла
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"
# Для запуска файла вне Django
# ----------------------------

django.setup()
from scraping.models import Vacancy


User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dct = {}
for i in qs:
    users_dct.setdefault((i['city'], i['language']), [])
    users_dct[(i['city'], i['language'])].append(i['email'])    # Получили словарь с составным ключом (город и ЯП), а значение - email

if users_dct:
    params = {'city_id__in': [], 'language_id__in': []}     # __ означает, что нужно найти все значения, которые принадлежат этой паре
    for pair in users_dct.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params)[:10]      # Ограничил десятью записями для теста. Позже надо будет взять объект datetime, чтоб посылать вакансии, взятые накануне


#----------------------------------------------------------------------------
# Формирование и отправка письма
# Используется библиотека from django.core.mail import EmailMultiAlternatives
subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'     # Заголовок письма, от кого, кому
text_content = 'This is an important message.'                              # Текстовый контент
html_content = '<p>This is an <strong>important</strong> message.</p>'      # html контент
msg = EmailMultiAlternatives(subject, text_content, from_email, [to])       # Создаём объект класса EmailMultiAlternatives, куда передаём необходимые параметры
msg.attach_alternative(html_content, "text/html")                           # Прикрепляем к письму необходимое содержимое
msg.send()                                                                  # Отправляем письмо
#----------------------------------------------------------------------------

