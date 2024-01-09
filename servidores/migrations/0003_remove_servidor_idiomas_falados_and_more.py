# Generated by Django 4.2.8 on 2024-01-09 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabelas_apoio', '0003_popular_idiomas'),
        ('servidores', '0002_alter_servidor_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servidor',
            name='idiomas_falados',
        ),
        migrations.AddField(
            model_name='servidor',
            name='idiomas_secundarios',
            field=models.ManyToManyField(blank=True, to='tabelas_apoio.idioma'),
        ),
    ]