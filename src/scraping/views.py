from django.shortcuts import render

from .forms import FindForm
from .models import Vacancy


#_____________________________________________#
# Страница home. Работа с базой данных, логика

def home_view(request):
    # print(request, 'POST')
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    qs = []
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        elif language:
            _filter['language__slug'] = language

        qs = Vacancy.objects.filter(**_filter)      # Не понял что такое **_filter!!!!!!!!!!!!!!!!!!
    return render(request, 'scraping/home.html', {'object_list': qs, 'form': form}) # Рендер самой страницы и передача в неё данных для отображения

# Страница home. Работа с базой данных, логика
#_____________________________________________#
