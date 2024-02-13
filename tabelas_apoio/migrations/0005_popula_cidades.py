from django.db import migrations
import pandas as pd
from django.conf import settings
import os

def carrega_dados_cidade(apps, schema_editor):
    Cidade = apps.get_model('tabelas_apoio', 'Cidade')
    Cidade.objects.all().delete()

    # Caminho para o arquivo CSV
    csv_file = os.path.join(settings.BASE_DIR, 'tabelas_apoio/dados_apoio/tabela_cidades_banco.csv')
    
    data_frame = pd.read_csv(csv_file)
    
    objs = [
        Cidade(
            id=row['id'],
            cod_ibge=row['cod_ibge'],
            cidade=row['cidade'],
            capital=row['capital'],
            codigo_uf=row['codigo_uf'],
            sigla_uf=row['sigla_uf'],
            uf=row['uf'],
            ddd=row['ddd'],
            fuso_horario=row['fuso_horario'],
            latitude=row['latitude'],
            longitude=row['longitude'],
            siafi_id=row['siafi_id'],
        )
        for index, row in data_frame.iterrows()
    ]
    Cidade.objects.bulk_create(objs)

class Migration(migrations.Migration):

    dependencies = [
        # Dependências necessárias, por exemplo:
        ('tabelas_apoio', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(carrega_dados_cidade),
    ]
