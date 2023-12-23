from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from utils import db_mandados, conector_ftp
from io import BytesIO
from datetime import datetime
from django.contrib import messages
import time

@login_required(login_url='/login/')
def cadastrar(request):
    
    nome = request.user.first_name
    sobrenome = request.user.last_name
    foto = request.user.foto

    usuario = f"{nome.capitalize()} {sobrenome.capitalize()}"

    context = {'user_name': usuario, 'foto': foto}

    return render(request, 'presos/cadastrar.html', context)