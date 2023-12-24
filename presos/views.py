from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from tabelas_apoio.models import Cidade
from utils import db_mandados, conector_ftp
from io import BytesIO
from datetime import datetime
from django.contrib import messages
import time
from .models import Preso
from django.utils.text import slugify
import base64
from django.core.files.base import ContentFile
import json



@login_required(login_url='/login/')
def cadastrar(request):
    if request.method == 'POST':
        novo_preso = Preso(
            data_fotos=request.POST.get('data_fotos'),
            origem_fotos=request.POST.get('origem_fotos'),
            nome_completo=request.POST.get('nome_completo'),
            data_nascimento=request.POST.get('data_nascimento'),
            mae=request.POST.get('mae'),
            pai=request.POST.get('pai'),
            rg=request.POST.get('rg'),
            uf_rg=request.POST.get('uf_rg'),
            cpf = request.POST.get('cpf', '').replace('.', '').replace('-', ''),
            cnh=request.POST.get('cnh'),
            nis=request.POST.get('nis'),
            sap=request.POST.get('sap'),
            razao_prisao=request.POST.get('razao_prisao'),
            numero_procedimento=request.POST.get('numero_procedimento'),
            observacao=request.POST.get('observacao'),
            created_by=request.user
        )
        
        novo_preso.save()

        for i in range(1, 4):
            image_data = request.POST.get(f'croppedImage{i}')
            if image_data:
                format, imgstr = image_data.split(';base64,') 
                ext = format.split('/')[-1] 
                image = ContentFile(base64.b64decode(imgstr), name=f'temp.{ext}')

                if i == 1:
                    novo_preso.perfil_esquerdo.save(f'{novo_preso.nome_completo}_esquerdo.{ext}', image)
                elif i == 2:
                    novo_preso.frontal.save(f'{novo_preso.nome_completo}_frontal.{ext}', image)
                elif i == 3:
                    novo_preso.perfil_direito.save(f'{novo_preso.nome_completo}_direito.{ext}', image)
        
        return HttpResponse("Preso cadastrado com sucesso!")
    
    nome = request.user.first_name
    sobrenome = request.user.last_name
    foto = request.user.foto

    ufs_unicos = Cidade.objects.values_list('uf', flat=True).distinct()
    ufs_unicos = sorted(ufs_unicos)

    usuario = f"{nome.capitalize()} {sobrenome.capitalize()}"

    return render(request, 'presos/cadastrar.html', {'user_name': usuario, 'foto': foto, 'ufs': ufs_unicos})