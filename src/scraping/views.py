from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import FindForm
from .models import Vacancy


def home_view(request):
    form = FindForm()

    return render(request, 'scraping/home.html', {'form': form}) # Рендер самой страницы и передача в неё данных для отображения



def list_view(request):
    # print(request, 'POST')
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    context = {'city': city, 'language': language, 'form': form}
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        elif language:
            _filter['language__slug'] = language

        qs = Vacancy.objects.filter(**_filter)      # Не понял что такое **_filter!!!!!!!!!!!!!!!!!!
        paginator = Paginator(qs, 10)  # Отображает 10 записей на странице.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] =  page_obj
    return render(request, 'scraping/list.html', context)
