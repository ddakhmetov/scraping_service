from django.contrib import admin
from django.urls import path, include
from scraping.views import home_view, list_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list', list_view, name='list'),   # name='name' нужно для относительных url
    path('accounts/', include(('accounts.urls', 'accounts'))),   # По порядку: 'accounts' - группа адресов; 'accounts.urls' - адреса. которые находятся в этой группе, смотреть там; 'acounts' - задаётся пространство имён
    path('', home_view, name='home'),   # При вводе адреса server/home выполняется функция home_view

]
