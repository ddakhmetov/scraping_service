from django.db import models


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
