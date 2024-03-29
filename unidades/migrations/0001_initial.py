# Generated by Django 4.2.10 on 2024-02-12 20:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AreasPC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_pc', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Cidades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_ibge', models.CharField(max_length=15, unique=True)),
                ('cidade', models.CharField(max_length=100)),
                ('regiao', models.CharField(choices=[('Interior', 'Interior'), ('Metropolitana', 'Metropolitana')], max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Unidades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_unidade', models.CharField(max_length=20, unique=True)),
                ('nome_unidade_policial', models.CharField(max_length=200)),
                ('sigla_unidade', models.CharField(max_length=50)),
                ('unidade_policial_ppe', models.CharField(max_length=200)),
                ('telefone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('area_pc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='unidades.areaspc')),
                ('cidade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='unidades.cidades')),
            ],
        ),
        migrations.CreateModel(
            name='Regional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regional', models.CharField(blank=True, max_length=200, null=True)),
                ('area_pc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='unidades.areaspc')),
            ],
        ),
    ]
