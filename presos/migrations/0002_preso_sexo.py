# Generated by Django 4.2.8 on 2023-12-24 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='preso',
            name='sexo',
            field=models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1, null=True),
        ),
    ]