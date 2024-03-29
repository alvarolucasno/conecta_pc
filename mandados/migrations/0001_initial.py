# Generated by Django 4.2.10 on 2024-02-12 20:22

from django.db import migrations, models
import mandados.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Procurados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(blank=True, null=True, upload_to=mandados.models.upload_face)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=mandados.models.upload_avatar)),
                ('origem_foto', models.CharField(max_length=255)),
                ('id_procurado_bnmp', models.BigIntegerField(unique=True)),
                ('nome_completo', models.CharField(max_length=255)),
                ('data_nascimento', models.DateField()),
                ('mae', models.CharField(max_length=255)),
                ('pai', models.CharField(blank=True, max_length=255, null=True)),
                ('rg', models.CharField(blank=True, max_length=20, null=True)),
                ('uf_rg', models.CharField(blank=True, max_length=100, null=True)),
                ('cpf', models.CharField(blank=True, max_length=14, null=True)),
                ('cnh', models.CharField(blank=True, max_length=20, null=True)),
                ('nis', models.CharField(blank=True, max_length=20, null=True)),
                ('sap', models.CharField(blank=True, max_length=10, null=True)),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1)),
                ('informacao_morte', models.BooleanField(default=False)),
                ('observacao', models.TextField(blank=True, null=True)),
                ('cpf_cadastrador', models.CharField(blank=True, max_length=14, null=True)),
                ('nome_cadastrador', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ativo', models.BooleanField(default=True)),
            ],
        ),
    ]
