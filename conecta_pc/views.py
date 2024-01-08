from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages

@login_required(login_url='/login/')
def home(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    foto = request.user.foto
    cargo = request.user.cargo

    user_name = f"{first_name.capitalize()} {last_name.capitalize()}"

    context = {'user_name': user_name, 'cargo': cargo, 'foto': foto}

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