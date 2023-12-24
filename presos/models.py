from django.conf import settings
from django.db import models
from django.utils.text import slugify

def upload_to_perfil_esquerdo(instance, filename):
    return f'presos/{slugify(instance.nome_completo)}_{slugify(instance.mae)}/{slugify(instance.nome_completo)}_{instance.data_fotos}_perfil_esquerdo.jpg'

def upload_to_frontal(instance, filename):
    return f'presos/{slugify(instance.nome_completo)}_{slugify(instance.mae)}/{slugify(instance.nome_completo)}_{instance.data_fotos}_face.jpg'

def upload_to_perfil_direito(instance, filename):
    return f'presos/{slugify(instance.nome_completo)}_{slugify(instance.mae)}/{slugify(instance.nome_completo)}_{instance.data_fotos}_perfil_direito.jpg'


class Preso(models.Model):
    # Fotos
    perfil_esquerdo = models.ImageField(upload_to=upload_to_perfil_esquerdo)
    frontal = models.ImageField(upload_to=upload_to_frontal)
    perfil_direito = models.ImageField(upload_to=upload_to_perfil_direito)
    
    # Datas e strings
    data_fotos = models.DateField()
    origem_fotos = models.CharField(max_length=255)
    nome_completo = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    mae = models.CharField(max_length=255)
    pai = models.CharField(max_length=255, blank=True, null=True)

    # Documentos
    rg = models.CharField(max_length=20, blank=True, null=True)
    uf_rg = models.CharField(max_length=100, blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    cnh = models.CharField(max_length=20, blank=True, null=True)
    nis = models.CharField(max_length=20, blank=True, null=True)
    sap = models.CharField(max_length=10, blank=True, null=True)
    
    SEXO_CHOICES = (
    ('M', 'Masculino'),
    ('F', 'Feminino'),
)
    
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)

    # Detalhes da prisão
    razao_prisao = models.CharField(max_length=255)
    numero_procedimento = models.CharField(max_length=50)
    observacao = models.TextField(blank=True, null=True)

    # Campos de controle
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome_completo

