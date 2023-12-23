from django.contrib import admin
from .models import AreasPC, Cidades, Unidades, Regional

@admin.register(AreasPC)
class AreasPCAdmin(admin.ModelAdmin):
    list_display = ['id', 'area_pc']
    search_fields = ['area_pc']

@admin.register(Regional)
class RegionalAdmin(admin.ModelAdmin):
    list_display = ['id', 'regional', 'area_pc']
    search_fields = ['regional']
    list_filter = ['area_pc']

@admin.register(Cidades)
class CidadesAdmin(admin.ModelAdmin):
    list_display = ['cod_ibge', 'cidade', 'regiao']
    search_fields = ['cidade', 'cod_ibge']
    list_filter = ['regiao']

@admin.register(Unidades)
class UnidadesAdmin(admin.ModelAdmin):
    list_display = ['codigo_unidade', 'nome_unidade_policial', 'sigla_unidade', 'cidade', 'area_pc', 'telefone', 'email']
    search_fields = ['nome_unidade_policial', 'codigo_unidade']
    list_filter = ['cidade__regiao', 'area_pc']
