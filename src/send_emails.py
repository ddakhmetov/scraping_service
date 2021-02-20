import os, sys
from django.contrib.auth import get_user_model
import django
import datetime
from django.core.mail import EmailMultiAlternatives


# ----------------------------
# Для запуска файла вне Django

proj = os.path.dirname(os.path.abspath('manage.py'))   #Для запуска файла вне Django. Узнаём абсолютный путь до файла
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"
# Для запуска файла вне Django
# ----------------------------

django.setup()
from scraping.models import Vacancy, Errors, Url_kz
# from scraping_service.settings import EMAIL_HOST_USER     # Если использовать dotenv
today = datetime.date.today()
subject = f'Рассылка вакансий за { today }'
text_content = f'Рассылка вакансий за { today }'
from_email = 'scraping.kz@gmail.com'    # EMAIL_HOST_USER      # Если использовать dotenv
ADMIN_USER = 'scraping.kz@gmail.com'    # EMAIL_HOST_USER      # Если использовать dotenv
empty = '<h2>К сожалению, на сегодня по Вашим предпочтениям данных нет :-(</h2>'
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
    qs = Vacancy.objects.filter(**params, timestamp=today).values()      # Ограничил десятью записями для теста. Позже надо будет взять объект datetime, чтоб посылать вакансии, взятые накануне
    vacancies = {}
    for i in qs:
        vacancies.setdefault((i['city_id'], i['language_id']), [])
        vacancies[(i['city_id'], i['language_id'])].append(i)
    for keys, emails in users_dct.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h3><a href="{ row["url"] }">{ row["title"] }</a></h3>'
            html += f'<p>{ row["description"] }</p>'
            html += f'<p>{ row["company"] }</p><br><hr><br>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [
                to])
            msg.attach_alternative(_html, "text/html")
            msg.send()


# #----------------------------------------------------------------------------
# # Формирование и отправка письма
# # Используется библиотека from django.core.mail import EmailMultiAlternatives
# subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'     # Заголовок письма, от кого, кому
# text_content = 'This is an important message.'                              # Текстовый контент
# html_content = '<p>This is an <strong>important</strong> message.</p>'      # html контент
# msg = EmailMultiAlternatives(subject, text_content, from_email, [to])       # Создаём объект класса EmailMultiAlternatives, куда передаём необходимые параметры
# msg.attach_alternative(html_content, "text/html")                           # Прикрепляем к письму необходимое содержимое
# msg.send()                                                                  # Отправляем письмо
# #----------------------------------------------------------------------------

qs = Errors.objects.filter(timestamp=today)
subject = ''
text_content = ''
to = ADMIN_USER
_html = ''
if qs.exists():
    error = qs.first()
    data = error.data
    for i in data:
        _html += f"<p><a href='{ i['url'] }'>Error: {i['title']}</a></p><br>"
    subject = f"Ошибки скрапинга { today }"
    text_content = f"Ошибки скрапинга { today }"
    qs = Url_kz.objects.all().values('city', 'language')
urls_dct = {(i['city'], i['language']): True for i in qs}
urls_err = ''
for keys in users_dct.keys():
    if keys not in urls_dct:
        urls_err += f"<p>Для города: { keys[0] } и языка программирования: { keys[1] } отсутствуют URLs</p><br>"
if urls_err:
    subject += ' Отсутствующие урлы'
    _html += urls_err

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [
        to])
    msg.attach_alternative(_html, "text/html")
    msg.send()
