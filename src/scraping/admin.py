from django.contrib import admin
from .models import City, Language, Vacancy, Errors, Url_kz#, Url_ua

admin.site.register(City)
admin.site.register(Language)
admin.site.register(Vacancy)
admin.site.register(Errors)
admin.site.register(Url_kz)
# admin.site.register(Url_ua)
