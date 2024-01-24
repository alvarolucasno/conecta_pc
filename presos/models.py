import os
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def upload_to_perfil_esquerdo(instance, filename):
    return f'presos/{slugify(instance.nome_completo)}_mae_{slugify(instance.mae)}/{instance.data_fotos}_perfil_esquerdo.jpg'

def upload_to_frontal(instance, filename):
    return f'presos/{slugify(instance.nome_completo)}_mae_{slugify(instance.mae)}/{instance.data_fotos}_face.jpg'

def upload_to_avatar(instance, filename):
    return f'presos/{slugify(instance.nome_completo)}_mae_{slugify(instance.mae)}/{instance.data_fotos}_avatar.jpg'

def upload_to_perfil_direito(instance, filename):
    return f'presos/{slugify(instance.nome_completo)}_mae_{slugify(instance.mae)}/{instance.data_fotos}_perfil_direito.jpg'

class Preso(models.Model):
    # Fotos
    perfil_esquerdo = models.ImageField(upload_to=upload_to_perfil_esquerdo, max_length=255)
    frontal = models.ImageField(upload_to=upload_to_frontal, max_length=255)
    avatar = models.ImageField(upload_to=upload_to_avatar, null=True, blank=True, max_length=255)
    perfil_direito = models.ImageField(upload_to=upload_to_perfil_direito, max_length=255)
    
    # Datas e strings
    data_fotos = models.DateField()
    origem_fotos = models.CharField(max_length=255)
    nome_completo = models.CharField(max_length=255)
    alcunha = models.CharField(max_length=255, blank=True, null=True)
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
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='presos_criados', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='presos_modificados', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome_completo
    
    def save(self, *args, **kwargs):
        # Verificar se as imagens foram atualizadas
        if self.pk:
            old_preso = Preso.objects.get(pk=self.pk)

            # Excluir imagens antigas se foram atualizadas
            if old_preso.perfil_esquerdo != self.perfil_esquerdo and old_preso.perfil_esquerdo:
                default_storage.delete(old_preso.perfil_esquerdo.path)
                self.compress_image(self.perfil_esquerdo)
            
            if old_preso.frontal != self.frontal and old_preso.frontal:
                default_storage.delete(old_preso.frontal.path)
                if old_preso.avatar:
                    default_storage.delete(old_preso.avatar.path)
                self.compress_image(self.frontal)
            
            if old_preso.perfil_direito != self.perfil_direito and old_preso.perfil_direito:
                default_storage.delete(old_preso.perfil_direito.path)
                self.compress_image(self.perfil_direito)

        else:
            # Novo objeto, processar todas as imagens
            if self.perfil_esquerdo:
                self.compress_image(self.perfil_esquerdo)
            if self.frontal:
                self.compress_image(self.frontal)
            if self.perfil_direito:
                self.compress_image(self.perfil_direito)

        # Salvar o objeto para garantir que todas as imagens sejam atualizadas
        super().save(*args, **kwargs)

        # Sempre criar um novo avatar se houver uma imagem frontal
        if self.frontal:
            if self.avatar:
                default_storage.delete(self.avatar.path)
            self.create_avatar()
            super().save(update_fields=['avatar'])

    def compress_image(self, image_field):
        # Abrir a imagem
        with Image.open(image_field) as image:

            # Converter imagem RGBA para RGB (se necessário)
            if image.mode == 'RGBA':
                image = image.convert('RGB')

            # Calcular o novo tamanho mantendo o aspect ratio
            max_resolution = 2000
            ratio = min(max_resolution / image.width, max_resolution / image.height)

            # Checar se é necessário redimensionar
            if ratio < 1:  # Redimensionar apenas se a imagem for maior que a resolução máxima
                size = (int(image.width * ratio), int(image.height * ratio))
                image = image.resize(size, Image.Resampling.LANCZOS)

            # Comprimir a imagem
            image_io = BytesIO()
            image.save(image_io, format='JPEG', quality=70)  # Ajustar a qualidade conforme necessário
            image_io.seek(0)

        # Salvar a imagem comprimida
        image_field.save(image_field.name, ContentFile(image_io.getvalue()), save=False)

    def create_avatar(self):
        if self.frontal:
            # Abrir a imagem frontal
            avatar_img = Image.open(self.frontal.path)

            # Calcular o novo tamanho mantendo o aspect ratio
            max_size = 200
            ratio = min(max_size / avatar_img.width, max_size / avatar_img.height)
            size = (int(avatar_img.width * ratio), int(avatar_img.height * ratio))
            avatar_img = avatar_img.resize(size, Image.Resampling.LANCZOS)

            # Converter para RGB se for RGBA (para suportar JPEG)
            if avatar_img.mode == 'RGBA':
                avatar_img = avatar_img.convert('RGB')

            # Preparar o arquivo temporário
            temp_thumb = BytesIO()
            avatar_img.save(temp_thumb, format='JPEG', quality=70)
            temp_thumb.seek(0)

            # Definir o nome do arquivo com extensão .jpeg
            avatar_name = os.path.splitext(self.frontal.name)[0] + '_avatar.jpeg'

            # Salvar o arquivo do avatar
            self.avatar.save(avatar_name, ContentFile(temp_thumb.read()), save=False)
            temp_thumb.close()


