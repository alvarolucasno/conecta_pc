from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Servidor, Cargo
from django.db.models import Max, OuterRef, Subquery
from django.shortcuts import render, redirect, get_object_or_404

@login_required(login_url='/login/')
def listar_servidores(request):
    
    cpf_do_usuario = request.user.cpf
    servidor = get_object_or_404(Servidor, cpf=cpf_do_usuario)
    cargo = get_object_or_404(Cargo, servidor=servidor, cargo_atual=True)
    foto = servidor.foto
    nome_completo = request.user.nome_completo.split()
    user_name = nome_completo[0] + ' ' + nome_completo[-1] if len(nome_completo) >= 2 else nome_completo[0]

    cargo_recente_subquery = Cargo.objects.filter(
            servidor=OuterRef('pk'),
            cargo_atual=True
        ).order_by('-created_at').values('pk')[:1]

    servidores = Servidor.objects.annotate(
        cargo_recente_id=Subquery(cargo_recente_subquery)
    )

    for servidor in servidores:
        if servidor.cargo_recente_id:
            cargo_recente = Cargo.objects.get(pk=servidor.cargo_recente_id)
            servidor.cargo_recente_nome = cargo_recente.cargo
        else:
            servidor.cargo_recente_nome = "Sem cargo"
    
    return render(request, 'servidores/listar_servidores.html', {'user_name': user_name, 'servidores': servidores, 'cargo': cargo.cargo, 'foto': foto})

@login_required(login_url='/login/')
def detalhar_servidor(request, servidor_id):
    
    cpf_do_usuario = request.user.cpf
    servidor = get_object_or_404(Servidor, cpf=cpf_do_usuario)
    cargo = get_object_or_404(Cargo, servidor=servidor, cargo_atual=True)
    foto = servidor.foto
    nome_completo = request.user.nome_completo.split()
    user_name = nome_completo[0] + ' ' + nome_completo[-1] if len(nome_completo) >= 2 else nome_completo[0]

    servidor = get_object_or_404(Servidor, pk=servidor_id)

    return render(request, 'servidores/detalhar_servidor.html', {'user_name': user_name, 'servidor': servidor, 'cargo': cargo.cargo, 'foto': foto})