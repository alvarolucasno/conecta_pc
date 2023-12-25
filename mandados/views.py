import base64
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from utils import db_mandados, conector_ftp, salvar_bot_telegram
from io import BytesIO
from datetime import datetime
from django.contrib import messages
import time
from tabelas_apoio.models import Cidade

@login_required(login_url='/login/')
def listar_alvos(request):
    
    nome = request.user.first_name
    sobrenome = request.user.last_name
    foto = request.user.foto

    mandados = db_mandados.get_mandados()

    usuario = f"{nome.capitalize()} {sobrenome.capitalize()}"

    context = {'user_name': usuario, 'foto': foto, 'dados': mandados}

    return render(request, 'mandados/listar_alvos.html', context)

@login_required(login_url='/login/')
def editar_alvo(request, id_pessoa):
    
    nome = request.user.first_name
    sobrenome = request.user.last_name
    nome_completo = request.user.nome_completo
    id_usuario = request.user.id
    cpf_usuario = request.user.cpf
    
    foto = request.user.foto

    usuario = f"{nome.capitalize()} {sobrenome.capitalize()}"
    
    ufs_unicos = Cidade.objects.values_list('sigla_uf', flat=True).distinct()
    ufs_unicos = sorted(ufs_unicos)
    
    id_alvo, nome_alvo = db_mandados.get_name_by_id(id_pessoa)
    
    if request.method == 'POST':
        try:
            origem_foto = str(request.POST.get('origemFoto')).strip()
            nome_alvo = ' '.join(str(request.POST.get('nomeCompleto')).split())
            dataNascimento = request.POST.get('dataNascimento') if request.POST.get('dataNascimento') else None
            mae = ' '.join(str(request.POST.get('mae')).split())
            pai = ' '.join(str(request.POST.get('pai')).split())
            rg = str(request.POST.get('rg')).strip()
            cpf = str(request.POST.get('cpf')).replace('.', '').replace('-', '').strip()
            cnh = str(request.POST.get('cnh')).strip()
            nis = str(request.POST.get('nis')).strip()
            sap = str(request.POST.get('sap')).strip()
            uf_rg = str(request.POST.get('uf_rg')).strip()
            data_cadastro = datetime.now()
            morto = request.POST.get('morto')
            observacao = str(request.POST.get('observacao')).strip()

            caminho_foto = None
            
            if 'fotografia' in request.FILES:
                fotografia = request.FILES['fotografia']
                file_obj = BytesIO(fotografia.read())
                nome_foto = (f"id_pessoa_bnmp_{id_alvo}_{nome_alvo}_mae_{mae}_dn_{dataNascimento}.jpg").replace(" ", "_")
                file_obj.seek(0)
                conector_ftp.enviar_foto_sftp(file_obj, nome_foto, 'fotos_alvos_banco')
                fotografia.seek(0)
                foto_base64 = base64.b64encode(fotografia.read()).decode('utf-8')
                informacao = f"Individuo com mandado de prisão em seu desfavor"
                salvar_bot_telegram.chamada_api(nome_alvo, dataNascimento, mae, foto_base64, informacao)

                caminho_foto = 'fotos_alvos_banco/' + nome_foto

            db_mandados.save_dados_alvo(id_alvo, nome_alvo, dataNascimento, mae, pai, rg, uf_rg, 
                                        cpf, cnh, nis, sap, caminho_foto, origem_foto, id_usuario, 
                                        nome_completo, cpf_usuario, data_cadastro, morto, observacao)
              
            messages.success(request, 'Dados salvos com sucesso!')
            return redirect('listar_alvos')
    
        except ValidationError as e:
            messages.error(request, f'Erro de validação: {e.message}')
        except Exception as e:
            messages.error(request, f'Erro ao salvar os dados: {e}')
    
    return render(request, 'mandados/editar_pessoa.html', {'user_name': usuario, 'foto': foto, 'id_alvo': id_alvo, 'nome_alvo': nome_alvo.upper(), 'ufs': ufs_unicos})