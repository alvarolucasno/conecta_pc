from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from servidores.models import Cargo, Servidor

@login_required(login_url='/login/')
def home(request):
    
    cpf_do_usuario = request.user.cpf
    servidor = get_object_or_404(Servidor, cpf=cpf_do_usuario)
    cargo = get_object_or_404(Cargo, servidor=servidor, cargo_atual=True)
    foto = servidor.foto
    nome_completo = request.user.nome_completo.split()
    user_name = nome_completo[0] + ' ' + nome_completo[-1] if len(nome_completo) >= 2 else nome_completo[0]

    context = {'user_name': user_name, 'cargo': cargo.cargo, 'foto': foto}

    return render(request, 'home/index.html', context)

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        password = request.POST['password']
        user = authenticate(request, username=usuario, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Login inválido. Tente novamente.")

    return render(request, 'login/login.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')



def teste(request):

    return render(request, 'home/teste.html')