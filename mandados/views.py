import base64
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from utils import db_mandados, conector_ftp, salvar_bot_telegram
from io import BytesIO
from datetime import datetime
from django.contrib import messages
import time
from tabelas_apoio.models import Cidade
from servidores.models import Cargo, Servidor
from mandados.models import Procurados
from utils.apoio_views import LISTA_DDDS, LISTA_UFS
from django.core.files.base import ContentFile
import base64


@login_required(login_url='/login/')
def listar_alvos(request):

    mandados = db_mandados.get_mandados()

    return render(request, 'mandados/listar_alvos.html', {'dados': mandados})

@login_required(login_url='/login/')
def editar_alvo(request, id_pessoa):
    
    nome_completo_cadastrador = request.user.nome_completo
    cpf_cadastrador = request.user.cpf
    
    id_foragido, nome_foragido = db_mandados.get_name_by_id(id_pessoa)
    
    if request.method == 'POST':
        try:
            origem_foto = request.POST.get('origemFoto')
            nome_procurado = ' '.join(str(request.POST.get('nomeCompleto')).split())
            dataNascimento = request.POST.get('dataNascimento') if request.POST.get('dataNascimento') else None
            mae = ' '.join(str(request.POST.get('mae')).split())
            pai = ' '.join(str(request.POST.get('pai')).split())
            rg = str(request.POST.get('rg')).strip()
            uf_rg = str(request.POST.get('uf_rg')).strip()
            cpf = str(request.POST.get('cpf')).replace('.', '').replace('-', '').strip()
            cnh = str(request.POST.get('cnh')).strip()
            nis = str(request.POST.get('nis')).strip()
            sap = str(request.POST.get('sap')).strip()
            sexo = str(request.POST.get('sexo')).strip()
            info_morte = request.POST.get('info_morte')
            observacao = str(request.POST.get('observacao')).strip()
            image_data = request.POST.get('croppedImage')
            
            if image_data:
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
            if imgstr:
                image = ContentFile(base64.b64decode(imgstr), name=f'{id_pessoa}.{ext}')

            procurado, created = Procurados.objects.get_or_create(
                id_procurado_bnmp = id_pessoa, 
                defaults={
                    'origem_foto': origem_foto,
                    'id_procurado_bnmp': id_pessoa,
                    'nome_completo': nome_procurado,
                    'data_nascimento': dataNascimento,
                    'mae': mae,
                    'pai': pai,
                    'rg': rg,
                    'uf_rg': uf_rg,
                    'cpf': cpf,
                    'cnh': cnh,
                    'nis': nis,
                    'sap': sap,
                    'sexo': sexo,
                    'informacao_morte': info_morte,
                    'observacao': observacao,
                    'cpf_cadastrador': cpf_cadastrador,
                    'nome_cadastrador': nome_completo_cadastrador,
                    'created_by': request.user,
                    'foto': image,
                }
            )
              
            if not created:
                procurado.origem_foto = origem_foto
                procurado.nome_completo = nome_procurado
                procurado.data_nascimento = dataNascimento
                procurado.mae = mae
                procurado.pai = pai
                procurado.rg = rg
                procurado.uf_rg = uf_rg
                procurado.cpf = cpf
                procurado.cnh = cnh
                procurado.nis = nis
                procurado.sap = sap
                procurado.sexo = sexo
                procurado.informacao_morte = info_morte
                procurado.observacao = observacao
                procurado.cpf_cadastrador = cpf_cadastrador
                procurado.nome_cadastrador = nome_completo_cadastrador
                procurado.updated_by = request.user
                procurado.foto = image
                procurado.save()
              
            messages.success(request, 'Dados salvos com sucesso!')
            return redirect('listar_alvos')
    
        except ValidationError as e:
            messages.error(request, f'Erro de validação: {e.message}')
        except Exception as e:
            messages.error(request, f'Erro ao salvar os dados: {e}')
    
    return render(request, 'mandados/editar_pessoa.html', {'id_alvo': id_foragido, 'nome_alvo': nome_foragido.upper(), 'ufs': LISTA_UFS})