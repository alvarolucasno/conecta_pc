# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    nome_completo = models.CharField(max_length=100, null=True, blank=True)
    cpf = models.CharField(
        max_length=11, 
        unique=True, 
        null=True,
        validators=[RegexValidator(r'^\d{11}$', 'CPF deve ter 11 dígitos.')]
    )
    SEXO_CHOICES = (
        ('F', 'Feminino'),
        ('M', 'Masculino'),
    )
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField(null=True, blank=True)
    cargo = models.CharField(max_length=100, null=True, blank=True)
    funcao = models.CharField(max_length=100, null=True, blank=True)
    foto = models.ImageField(upload_to='fotos_usuarios/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
