# Generated by Django 3.1.4 on 2021-02-05 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название населённого пункта')),
                ('slug', models.CharField(blank=True, max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Название населённого пункта',
                'verbose_name_plural': 'Название населённых пунктов',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Язык программирования')),
                ('slug', models.CharField(blank=True, max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Язык программирования',
                'verbose_name_plural': 'Языки программирования',
            },
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True)),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок вакансии')),
                ('company', models.CharField(max_length=255, verbose_name='Компания')),
                ('description', models.TextField(verbose_name='Описание вакансии')),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.city', verbose_name='Город')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.language', verbose_name='Язык программирования')),
            ],
            options={
                'verbose_name': 'Вакансия',
                'verbose_name_plural': 'Вакансии',
            },
        ),
    ]
