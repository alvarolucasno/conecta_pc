# users/models.py
from io import BytesIO
import os
from django.conf import settings
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from PIL import Image
from django.core.validators import RegexValidator
from unidades.models import Unidades
from tabelas_apoio.models import Idioma
from users.models import CustomUser

def upload_foto_servidor(instance, filename):
    return f'fotos_servidores/{slugify(instance.nome_completo)}_cpf_{slugify(instance.cpf)}/{instance.created_at.strftime("%Y-%m-%d")}_foto.jpg'

def upload_avatar_servidor(instance, filename):
    return f'fotos_servidores/{slugify(instance.nome_completo)}_cpf_{slugify(instance.cpf)}/{instance.created_at.strftime("%Y-%m-%d")}_avatar.jpg'

class Servidor(models.Model):
    
    # DADOS PESSOAIS
    nome_completo = models.CharField(max_length=250, null=True, blank=True)
    nome_guerra = models.CharField(max_length=250, null=True, blank=True)
    nome_mae = models.CharField(max_length=250, null=True, blank=True)
    nome_pai = models.CharField(max_length=250, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    uf_naturalidade = models.CharField(max_length=250, null=True, blank=True)
    naturalidade = models.CharField(max_length=250, null=True, blank=True)
    cpf = models.CharField(
        max_length=250, 
        unique=True, 
        null=True, 
        validators=[RegexValidator(r'^\d{11}$', 'CPF deve ter 11 dígitos.')]
    )
    rg = models.CharField(max_length=250, null=True, blank=True)
    uf_rg = models.CharField(max_length=250, null=True, blank=True)
    cnh = models.CharField(max_length=250, null=True, blank=True)
    categoria_cnh = models.CharField(max_length=250, null=True, blank=True)
    primeira_habilitacao = models.DateField(null=True, blank=True)
    vencimento_habilitacao = models.DateField(null=True, blank=True)
    pis_pasep = models.CharField(max_length=250, null=True, blank=True)
    titulo_eleitor = models.CharField(max_length=250, null=True, blank=True)
    zona_eleitoral = models.CharField(max_length=250, null=True, blank=True)
    secao_eleitoral = models.CharField(max_length=250, null=True, blank=True)
    estado_civil = models.CharField(max_length=250, null=True, blank=True)
    tipo_sanguineo = models.CharField(max_length=250, null=True, blank=True)
    cor_pele = models.CharField(max_length=250, null=True, blank=True)
    sexo = models.CharField(max_length=250, choices=[('F', 'Feminino'), ('M', 'Masculino')], null=True)
    nacionalidade = models.CharField(max_length=250, null=True, blank=True)
    
    # FOTO
    foto = models.ImageField(upload_to=upload_foto_servidor, null=True, blank=True)
    avatar = models.ImageField(upload_to=upload_avatar_servidor, null=True, blank=True)
    
    # CONTATOS
    email_funcional = models.EmailField(unique=True)
    email_secundario = models.EmailField(null=True, blank=True)
    telefone_whatsapp = models.CharField(max_length=250, null=True, blank=True)
    telefone_secundario = models.CharField(max_length=250, null=True, blank=True)
    pessoa_emergencia = models.CharField(max_length=250, null=True, blank=True)
    relacao_pessoa_emergencia = models.CharField(max_length=250, null=True, blank=True)
    telefone_pessoa_emergencia = models.CharField(max_length=250, null=True, blank=True)  

    # INFORMAÇÕES ADICIONAIS
    situacao_servidor = models.CharField(max_length=250, null=True, blank=True)
    horario_reduzido = models.BooleanField(default=False)
    motivo_horario_reduzido = models.CharField(max_length=250, null=True, blank=True)
    data_inicio_horario_reduzido = models.DateField(null=True, blank=True)
    escolaridade = models.CharField(max_length=250, null=True, blank=True)
    religiao = models.CharField(max_length=250, null=True, blank=True)
    idiomas_secundarios = models.ManyToManyField(Idioma, blank=True)
    tamanho_camisa = models.CharField(max_length=250, null=True, blank=True)
    tamanho_colete = models.CharField(max_length=250, null=True, blank=True)
    tamanho_calca = models.CharField(max_length=250, null=True, blank=True)
    tamanho_calcado = models.CharField(max_length=250, null=True, blank=True)
    quantidade_filhos = models.IntegerField(null=True, blank=True)
    deficiencia = models.BooleanField(default=False)
    tipo_deficiencia = models.CharField(max_length=250, null=True, blank=True)
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='usuario_criado', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='usuario_modificado', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Servidor'
        verbose_name_plural = 'Servidores'

    def __str__(self):
        return self.nome_completo
    
    def save(self, *args, **kwargs):

        if self.foto:
            self.compress_image(self.foto)

        if self.foto and not self.avatar:
            self.create_avatar()

        super().save(*args, **kwargs)

        if not CustomUser.objects.filter(cpf=self.cpf).exists():
            email_funcional = self.email_funcional

            # Criar um novo usuário com os dados do Servidor
            CustomUser.objects.create_user(
                email_funcional=email_funcional,
                nome_completo=self.nome_completo,
                cpf=self.cpf,
                password=self.cpf
            )
        else:
            pass     

    def compress_image(self, image_field):
        image = Image.open(image_field)

        if image.mode == 'RGBA':
            image = image.convert('RGB')

        image_io = BytesIO()
        image.save(image_io, format='JPEG', quality=70)
        
        image_field.save(image_field.name, ContentFile(image_io.getvalue()), save=False)

    def create_avatar(self):
        if self.foto:
            avatar_img = Image.open(self.foto.path)

            max_size = 100
            ratio = min(max_size / avatar_img.width, max_size / avatar_img.height)
            size = (int(avatar_img.width * ratio), int(avatar_img.height * ratio))
            avatar_img = avatar_img.resize(size, Image.Resampling.LANCZOS)

            if avatar_img.mode == 'RGBA':
                avatar_img = avatar_img.convert('RGB')

            temp_thumb = BytesIO()
            avatar_img.save(temp_thumb, format='JPEG', quality=70)
            temp_thumb.seek(0)

            avatar_name = os.path.splitext(self.foto.name)[0] + '_avatar.jpeg'

            self.avatar.save(avatar_name, ContentFile(temp_thumb.read()), save=False)
            temp_thumb.close()

    
class Cargo(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete=models.SET_NULL, null=True)
    tipo_vinculo = models.CharField(max_length=250, null=True, blank=True) #COMISSIONADO OU EFETIVO
    cargo = models.CharField(max_length=250, null=True, blank=True)
    cargo_atual = models.BooleanField(default=True)
    data_inicio_vinculo = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='cargo_criado', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='cargo_modificado', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)

class Classe(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete=models.SET_NULL, null=True)
    classe = models.CharField(max_length=250, null=True, blank=True)
    classe_acesso = models.BooleanField(default=False)
    classe_final = models.BooleanField(default=False)
    data_classe = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='classe_atribuida', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='classe_modificada', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)

class Lotacao(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete=models.SET_NULL, null=True)
    tipo_local_trabalho = models.CharField(max_length=250, null=True, blank=True)
    modalidade_lotacao = models.CharField(max_length=250, null=True, blank=True) #A PEDIDO, EX_OFICIO, ORDEM JUDICIAL
    lotacao = models.ForeignKey(Unidades, on_delete=models.SET_NULL, null=True, blank=True)
    funcao = models.CharField(max_length=250, null=True, blank=True)
    observacao = models.TextField(null=True, blank=True)
    data_lotacao = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='lotacao_atribuida', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='lotacao_modificada', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Honraria(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete=models.SET_NULL, null=True)
    honraria = models.CharField(max_length=250, null=True, blank=True)
    origem = models.CharField(max_length=250, null=True, blank=True)
    data_concessao = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='honraria_incluida', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='honraria_modificada', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class AnotacaoElogiosa(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete=models.SET_NULL, null=True)
    anotacao_elogiosa = models.TextField(null=True, blank=True)
    origem = models.CharField(max_length=250, null=True, blank=True)
    data_anotacao = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='anotacao_elogiosa_incluida', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='anotacao_elogiosa_modificada', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)

class Punicao(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete=models.SET_NULL, null=True)
    punicao = models.CharField(max_length=250, null=True, blank=True)
    infracoes = models.TextField(null=True, blank=True)
    data_punicao = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='punicao_incluida', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='punicao_modificada', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Restricao(models.Model):
    servidor = models.ForeignKey(Servidor, on_delete=models.SET_NULL, null=True)
    origem_restricao = models.CharField(max_length=250, null=True, blank=True)
    restricao = models.DateField(null=True, blank=True)
    data_restricao = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='restricao_incluida', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='restricao_modificada', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)