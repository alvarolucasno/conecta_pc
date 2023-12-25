import requests
import json

url = 'http://38.242.248.229:8118/cadastrar_pessoa/'

def chamada_api(nome, data_nascimento, nome_mae, foto, informacao):
    dados = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "nome_mae": nome_mae,
        "foto": foto,
        "informacao": informacao,
    }

    requests.post(url, json=dados)
