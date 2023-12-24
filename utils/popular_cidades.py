import csv
from tabelas_apoio.models import Cidade

def run():
    with open(r'C:\Users\ALVAR\OneDrive\Polícia\tabela_cidades_banco.csv', encoding='utf-8', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            obj, created = Cidade.objects.get_or_create(
                id=row['id'],
                defaults={
                    'cod_ibge': row['cod_ibge'],
                    'cidade': row['cidade'],
                    'capital': bool(int(row['capital'])),
                    'codigo_uf': row['codigo_uf'],
                    'sigla_uf': row['sigla_uf'],
                    'uf': row['uf'],
                    'ddd': row['ddd'],
                    'fuso_horario': row['fuso_horario'],
                    'latitude': float(row['latitude']),
                    'longitude': float(row['longitude']),
                    'siafi_id': row['siafi_id'],
                }
            )

run()



#python manage.py shell
#from utils.popular_cidades import run
#run()