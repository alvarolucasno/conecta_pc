#users/models.py

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email_funcional, nome_completo, cpf, password=None, **extra_fields):
        if not email_funcional:
            raise ValueError('O e-mail funcional é obrigatório')
        user = self.model(
            email_funcional=email_funcional,
            nome_completo=nome_completo,
            cpf=cpf,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_funcional, nome_completo, cpf, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True.')

        return self.create_user(email_funcional, nome_completo, cpf, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    nome_completo = models.CharField(max_length=100)
    cpf = models.CharField(
        max_length=11, 
        unique=True, 
        validators=[RegexValidator(r'^\d{11}$', 'CPF deve ter 11 dígitos.')]
    )
    email_funcional = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email_funcional'
    REQUIRED_FIELDS = ['nome_completo', 'cpf']

    objects = CustomUserManager()
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.email_funcional
