from django.db import models
# import jsonfield

from scraping.urls import from_cyrillic_to_eng



class City(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name="Название населённого пункта",
                            unique=True)  #Charfield в отличие от TextField такое текстовое поле, которое ограничивается количеством символов
    slug = models.CharField(max_length=50, blank=True, unique=True)  #blank=True означает, что поле может быть пустое
    
    class Meta:
        verbose_name = 'Название населённого пункта'    #Отображение имени таблицы в едиственном числе
        verbose_name_plural = 'Название населённых пунктов'     #Отображение имени таблицы во множественном числе

    def __str__(self):
        return self.name    # Отображение объекта в виде имени города

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name="Язык программирования",
                            unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255, verbose_name='Заголовок вакансии')
    company = models.CharField(max_length=255, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание вакансии')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 verbose_name='Язык программирования')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return self.title


class Errors(models.Model):

    timestamp = models.DateField(auto_now_add=True)
    data = models.JSONField()
    
    class Meta:
        verbose_name = 'Ошибка'
        verbose_name_plural = 'Ошибки'
