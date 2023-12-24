from django.db import models

class Cidade(models.Model):
    id = models.IntegerField(primary_key=True)
    cod_ibge = models.IntegerField()
    cidade = models.CharField(max_length=100)
    capital = models.BooleanField()
    codigo_uf = models.IntegerField()
    sigla_uf = models.CharField(max_length=2)
    uf = models.CharField(max_length=100)
    ddd = models.IntegerField()
    fuso_horario = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    siafi_id = models.IntegerField()

    def __str__(self):
        return self.cidade
