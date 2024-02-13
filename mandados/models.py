from django.db import models

# Create your models here.
import os
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils import timezone
import datetime

def upload_face(instance, filename):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    return f'fotos_procurados/{slugify(instance.id_procurado_bnmp)}/{timestamp}.jpg'

def upload_avatar(instance, filename):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    return f'fotos_procurados/{slugify(instance.id_procurado_bnmp)}/{timestamp}_avatar.jpg'

class Procurados(models.Model):
    foto = models.ImageField(upload_to=upload_face, null=True, blank=True)
    avatar = models.ImageField(upload_to=upload_avatar, null=True, blank=True)
    origem_foto = models.CharField(max_length=255, blank=True, null=True)
    id_procurado_bnmp = models.BigIntegerField(unique=True)
    nome_completo = models.CharField(max_length=255)
    data_nascimento = models.DateField(blank=True, null=True)
    mae = models.CharField(max_length=255)
    pai = models.CharField(max_length=255, blank=True, null=True)
    # Documentos
    rg = models.CharField(max_length=255, blank=True, null=True)
    uf_rg = models.CharField(max_length=100, blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    cnh = models.CharField(max_length=255, blank=True, null=True)
    nis = models.CharField(max_length=255, blank=True, null=True)
    sap = models.CharField(max_length=255, blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=(('M', 'Masculino'), ('F', 'Feminino')))
    informacao_morte = models.BooleanField(default=False, blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)
    # Campos de controle
    cpf_cadastrador = models.CharField(max_length=14, blank=True, null=True)
    nome_cadastrador = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='procurados_criados', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='procurados_modificados', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return self.nome_completo
    
    def save(self, *args, **kwargs):
        if self.pk:
            if 'update_fields' not in kwargs or 'foto' in kwargs.get('update_fields', []):
                self.update_image_files()

        else:
            if self.foto:
                self.compress_image(self.foto)
                self.create_avatar()

        super().save(*args, **kwargs)
        
    def update_image_files(self):
        old_instance = Procurados.objects.get(pk=self.pk)
        if old_instance.foto.name != self.foto.name:
            if old_instance.foto:
                default_storage.delete(old_instance.foto.path)
            if old_instance.avatar:
                default_storage.delete(old_instance.avatar.path)
            self.compress_image(self.foto)
            self.create_avatar()

    def compress_image(self, image_field):
        with Image.open(image_field) as image:
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            max_resolution = 2000
            ratio = min(max_resolution / image.width, max_resolution / image.height)
            if ratio < 1:
                size = (int(image.width * ratio), int(image.height * ratio))
                image = image.resize(size, Image.Resampling.LANCZOS)
            image_io = BytesIO()
            image.save(image_io, format='JPEG', quality=70)
            image_io.seek(0)
        image_field.save(image_field.name, ContentFile(image_io.getvalue()), save=False)

    def create_avatar(self):
        if self.foto:
            avatar_img = Image.open(self.foto.path)
            max_size = 200
            ratio = min(max_size / avatar_img.width, max_size / avatar_img.height)
            size = (int(avatar_img.width * ratio), int(avatar_img.height * ratio))
            avatar_img = avatar_img.resize(size, Image.Resampling.LANCZOS)
            if avatar_img.mode == 'RGBA':
                avatar_img = avatar_img.convert('RGB')
            temp_thumb = BytesIO()
            avatar_img.save(temp_thumb, format='JPEG', quality=70)
            temp_thumb.seek(0)
            avatar_name = f'{os.path.splitext(os.path.basename(self.foto.name))[0]}_avatar.jpeg'
            self.avatar.save(avatar_name, ContentFile(temp_thumb.getvalue()), save=False)