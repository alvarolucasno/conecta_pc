from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from servidores.models import Cargo, Servidor

@login_required(login_url='/login/')
def home(request):

    return render(request, 'home/index.html')

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        password = request.POST['password']
        user = authenticate(request, username=usuario, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Login inválido. Tente novamente.")
            return render(request, 'login/login.html')

    return render(request, 'login/login.html')

def logout_view(request):
    logout(request)
    return redirect('/login/')

def teste(request):

    return render(request, 'home/teste.html')