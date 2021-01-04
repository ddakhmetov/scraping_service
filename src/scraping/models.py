from django.db import models


class City(models.Model):
    name = models.CharField(max_length=50) #Charfield в отличие от TextField такое текстовое поле, которое ограничивается количеством символов
    slug = models.CharField(max_length=50, blank=True) #blank=True означает, что поле может быть пустое
