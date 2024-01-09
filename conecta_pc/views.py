from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages

@login_required(login_url='/login/')
def home(request):
    
    cargo = "Agente de Polícia Civil"
    nome_completo = request.user.nome_completo.split()
    user_name = nome_completo[0] + ' ' + nome_completo[-1] if len(nome_completo) >= 2 else nome_completo[0]

    context = {'user_name': user_name, 'cargo': cargo}

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