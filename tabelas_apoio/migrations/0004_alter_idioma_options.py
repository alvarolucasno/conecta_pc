# Generated by Django 4.2.9 on 2024-01-20 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tabelas_apoio', '0003_popular_idiomas'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='idioma',
            options={'ordering': ['nome'], 'verbose_name': 'idioma', 'verbose_name_plural': 'idiomas'},
        ),
    ]