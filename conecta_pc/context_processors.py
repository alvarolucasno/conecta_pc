from django.shortcuts import get_object_or_404
from servidores.models import Servidor, Cargo 

def dados_usuario(request):
    if request.user.is_authenticated:
        cpf_do_usuario = request.user.cpf
        servidor = Servidor.objects.filter(cpf=cpf_do_usuario).first()
        cargo = Cargo.objects.filter(servidor=servidor, cargo_atual=True).first() if servidor else None
        foto = servidor.foto if servidor else None
        nome_completo = request.user.nome_completo.split()
        user_name = nome_completo[0] + ' ' + nome_completo[-1] if len(nome_completo) >= 2 else nome_completo[0]
        
        return {
            'cpf_do_usuario': cpf_do_usuario,
            'servidor': servidor,
            'cargo': cargo.cargo,
            'foto': foto,
            'user_name': user_name,
        }
    else:
        return {}