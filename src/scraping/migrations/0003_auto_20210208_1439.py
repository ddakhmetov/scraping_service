# Generated by Django 3.1.4 on 2021-02-08 14:39

from django.db import migrations, models
import django.db.models.deletion
import scraping.models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0002_errors'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='errors',
            options={'verbose_name': 'Ошибка', 'verbose_name_plural': 'Ошибки'},
        ),
        migrations.CreateModel(
            name='Url_ua',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_data_ua', models.JSONField(default=scraping.models.default_urls_ua)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.city', verbose_name='Город')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.language', verbose_name='Язык программирования')),
            ],
            options={
                'unique_together': {('city', 'language')},
            },
        ),
        migrations.CreateModel(
            name='Url_kz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_data_kz', models.JSONField(default=scraping.models.default_urls_kz)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.city', verbose_name='Город')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.language', verbose_name='Язык программирования')),
            ],
            options={
                'unique_together': {('city', 'language')},
            },
        ),
    ]
