# unidades/models.py
from django.db import models

class AreasPC(models.Model):
    area_pc = models.CharField(max_length=200)

    def __str__(self):
        return self.area_pc
    
class Regional(models.Model):
    regional = models.CharField(max_length=200, null=True, blank=True)
    area_pc = models.ForeignKey(AreasPC, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.regional

class Cidades(models.Model):
    REGIAO_CHOICES = (
        ('Interior', 'Interior'),
        ('Metropolitana', 'Metropolitana'),
    )

    cod_ibge = models.CharField(max_length=15, unique=True)
    cidade = models.CharField(max_length=100)
    regiao = models.CharField(max_length=15, choices=REGIAO_CHOICES)

    def __str__(self):
        return self.cidade

class Unidades(models.Model):
    codigo_unidade = models.CharField(max_length=20, unique=True)
    nome_unidade_policial = models.CharField(max_length=200)
    sigla_unidade = models.CharField(max_length=50)
    unidade_policial_ppe = models.CharField(max_length=200)
    cidade = models.ForeignKey(Cidades, on_delete=models.SET_NULL, null=True, blank=True)
    area_pc = models.ForeignKey(AreasPC, on_delete=models.SET_NULL, null=True, blank=True)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nome_unidade_policial} - ({self.sigla_unidade})"


