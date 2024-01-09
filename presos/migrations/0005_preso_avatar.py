# Generated by Django 4.2.9 on 2024-01-09 14:19

from django.db import migrations, models
import presos.models


class Migration(migrations.Migration):

    dependencies = [
        ('presos', '0004_preso_updated_by_alter_preso_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='preso',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=presos.models.upload_to_avatar),
        ),
    ]
