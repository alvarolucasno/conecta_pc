from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from tabelas_apoio.models import Cidade
from utils import db_mandados, conector_ftp, salvar_bot_telegram
from io import BytesIO
from datetime import datetime
from django.contrib import messages
import time
from .models import Preso
from django.utils.text import slugify
import base64
from django.core.files.base import ContentFile
import json
from .models import Preso
from servidores.models import Cargo, Servidor

@login_required(login_url='/login/')
def listar_presos(request):
    
    cpf_do_usuario = request.user.cpf
    servidor = get_object_or_404(Servidor, cpf=cpf_do_usuario)
    cargo = get_object_or_404(Cargo, servidor=servidor, cargo_atual=True)
    foto = servidor.foto
    nome_completo = request.user.nome_completo.split()
    user_name = nome_completo[0] + ' ' + nome_completo[-1] if len(nome_completo) >= 2 else nome_completo[0]

    lista_presos = Preso.objects.filter(ativo=True)

    return render(request, 'presos/listar_presos.html', {
        'user_name': user_name,
        'presos': lista_presos,
        'cargo': cargo.cargo, 
        'foto': foto
    })
    
@login_required(login_url='/login/')
def cadastrar_preso(request):
    
    cpf_do_usuario = request.user.cpf
    servidor = get_object_or_404(Servidor, cpf=cpf_do_usuario)
    cargo = get_object_or_404(Cargo, servidor=servidor, cargo_atual=True)
    foto = servidor.foto
    nome_completo = request.user.nome_completo.split()
    user_name = nome_completo[0] + ' ' + nome_completo[-1] if len(nome_completo) >= 2 else nome_completo[0]

    ufs_unicos = Cidade.objects.values_list('uf', flat=True).distinct()
    ufs_unicos = sorted(ufs_unicos)
    
    if request.method == 'POST':
        
        nome_completo = ' '.join(request.POST.get('nome_completo', '').split())
        data_fotos = request.POST.get('data_fotos')

        # Verificar se já existe um preso com o mesmo nome e data das fotos
        preso_existente = Preso.objects.filter(nome_completo=nome_completo, data_fotos=data_fotos).first()
        if preso_existente:
            messages.error(request, 'Já existe um cadastro para este preso com a mesma data de fotos.')
            return render(request, 'presos/cadastrar.html', {'user_name': user_name, 'cargo': cargo.cargo, 'foto': foto, 'ufs': ufs_unicos})

        try:
            novo_preso = Preso(
                data_fotos=data_fotos,
                origem_fotos=request.POST.get('origem_fotos'),
                sexo=request.POST.get('sexo'),
                nome_completo=nome_completo,
                alcunha = ' '.join(request.POST.get('alcunha', '').split()),
                data_nascimento=request.POST.get('data_nascimento'),
                mae=' '.join(request.POST.get('mae', '').split()),
                pai=' '.join(request.POST.get('pai', '').split()),
                rg=request.POST.get('rg', '').strip(),
                uf_rg=request.POST.get('uf_rg'),
                cpf=request.POST.get('cpf', '').replace('.', '').replace('-', ''),
                cnh=request.POST.get('cnh', '').strip(),
                nis=request.POST.get('nis', '').strip(),
                sap=request.POST.get('sap', '').strip(),
                razao_prisao=request.POST.get('razao_prisao'),
                numero_procedimento=request.POST.get('numero_procedimento', '').strip(),
                observacao=request.POST.get('observacao', '').strip(),
                created_by=request.user
            )

            # Processamento de imagens
            imagens_processadas = False
            for i in range(1, 4):
                image_data = request.POST.get(f'croppedImage{i}')
                if image_data:
                    format, imgstr = image_data.split(';base64,') 
                    ext = format.split('/')[-1] 
                    image = ContentFile(base64.b64decode(imgstr), name=f'temp.{ext}')

                    if i == 1:
                        novo_preso.perfil_esquerdo = image
                    elif i == 2:
                        novo_preso.frontal = image
                    elif i == 3:
                        novo_preso.perfil_direito = image
                    
                    imagens_processadas = True

            if imagens_processadas:
                novo_preso.save()
            
            informacao = f"Individuo preso em virtude do(a) {novo_preso.razao_prisao} nº {novo_preso.numero_procedimento}"
            salvar_bot_telegram.chamada_api(novo_preso.nome_completo, novo_preso.data_nascimento, novo_preso.mae, (request.POST.get(f'croppedImage{2}').split(';base64,')[1]), informacao)
            messages.success(request, 'Dados salvos com sucesso!')
            return redirect('listar_presos')
        
        except ValidationError as e:
            messages.error(request, f'Erro de validação: {e.message}')
        except Exception as e:
            messages.error(request, f'Erro ao salvar os dados: {e}')

    return render(request, 'presos/cadastrar.html', {'user_name': user_name, 'cargo': cargo.cargo, 'foto': foto, 'ufs': ufs_unicos})

@login_required(login_url='/login/')
def editar_preso(request, preso_id):
    
    cpf_do_usuario = request.user.cpf
    servidor = get_object_or_404(Servidor, cpf=cpf_do_usuario)
    cargo = get_object_or_404(Cargo, servidor=servidor, cargo_atual=True)
    foto = servidor.foto
    nome_completo = request.user.nome_completo.split()
    user_name = nome_completo[0] + ' ' + nome_completo[-1] if len(nome_completo) >= 2 else nome_completo[0]

    ufs_unicos = Cidade.objects.values_list('uf', flat=True).distinct()
    ufs_unicos = sorted(ufs_unicos)
    
    preso = get_object_or_404(Preso, id=preso_id)
    
    if request.method == 'POST':
        try:
            # Atualiza os campos do preso com os dados do formulário
            preso.data_fotos = request.POST.get('data_fotos')
            preso.origem_fotos = request.POST.get('origem_fotos')
            preso.nome_completo = ' '.join(request.POST.get('nome_completo', '').split())
            preso.alcunha = ' '.join(request.POST.get('alcunha', '').split())
            preso.sexo = request.POST.get('sexo')
            preso.data_nascimento = request.POST.get('data_nascimento')
            preso.mae = ' '.join(request.POST.get('mae', '').split())
            preso.pai = ' '.join(request.POST.get('pai', '').split())
            preso.rg = request.POST.get('rg', '').strip()
            preso.uf_rg = request.POST.get('uf_rg')
            preso.cpf = request.POST.get('cpf', '').replace('.', '').replace('-', '')
            preso.cnh = request.POST.get('cnh', '').strip()
            preso.nis = request.POST.get('nis', '').strip()
            preso.sap = request.POST.get('sap', '').strip()
            preso.razao_prisao = request.POST.get('razao_prisao')
            preso.numero_procedimento = request.POST.get('numero_procedimento', '').strip()
            preso.observacao = request.POST.get('observacao', '').strip()
            preso.updated_by = request.user

            # Processamento de imagens
            for i in range(1, 4):
                image_data = request.POST.get(f'croppedImage{i}')
                if image_data:
                    format, imgstr = image_data.split(';base64,') 
                    ext = format.split('/')[-1] 
                    image = ContentFile(base64.b64decode(imgstr), name=f'temp.{ext}')

                    if i == 1:
                        preso.perfil_esquerdo = image
                    elif i == 2:
                        preso.frontal = image
                    elif i == 3:
                        preso.perfil_direito = image
                  
            preso.save()

            messages.success(request, 'Preso atualizado com sucesso!')
            return redirect('listar_presos')

        except Exception as e:
            messages.error(request, f'Erro ao atualizar os dados: {e}')

    return render(request, 'presos/editar_preso.html', {
        'user_name': user_name,
        'ufs': ufs_unicos,
        'preso': preso,
        'cargo': cargo.cargo, 
        'foto': foto
    })

@login_required(login_url='/login/')
def exibir_preso(request, preso_id):
    
    cpf_do_usuario = request.user.cpf
    servidor = get_object_or_404(Servidor, cpf=cpf_do_usuario)
    cargo = get_object_or_404(Cargo, servidor=servidor, cargo_atual=True)
    foto = servidor.foto
    nome_completo = request.user.nome_completo.split()
    user_name = nome_completo[0] + ' ' + nome_completo[-1] if len(nome_completo) >= 2 else nome_completo[0]

    ufs_unicos = Cidade.objects.values_list('uf', flat=True).distinct()
    ufs_unicos = sorted(ufs_unicos)
    
    preso = get_object_or_404(Preso, id=preso_id)
    
    return render(request, 'presos/exibir_preso.html', {
        'user_name': user_name,
        'ufs': ufs_unicos,
        'preso': preso,
        'cargo': cargo.cargo, 
        'foto': foto
    })

@login_required(login_url='/login/')
@require_POST
def excluir_preso(request, preso_id):
    preso = get_object_or_404(Preso, id=preso_id)
    preso.ativo = False 
    preso.save()
    messages.success(request, 'Preso excluído com sucesso.')
    return redirect('listar_presos')