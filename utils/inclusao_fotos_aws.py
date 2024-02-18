import os
import sys
import django

# Ajuste o caminho abaixo conforme a localização do seu projeto Django
caminho_projeto = "c:/Users/ALVAR/Documents/Projetos Python/conecta_pc"
sys.path.append(caminho_projeto)

import mysql.connector
import requests
from reconhecimento_facial.utils import adicionar_face

DB_CONFIG = {
    'host': '38.242.248.229',
    'user': 'alvaro',
    'password': '33441065',
}

database = 'conecta_pc'

def carregar_imagem(caminho_imagem):
    resposta = requests.get(caminho_imagem)
    if resposta.status_code == 200:
        print(f"Imagem carregada com sucesso: {caminho_imagem}")
        return resposta.content
    else:
        print(f"Erro ao carregar a imagem: {caminho_imagem}")
        return None

def atualizar_face_id_aws_no_banco(face_id_aws, id_preso):
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            sql_update_query = f"""UPDATE {database}.presos_preso SET face_id_aws = %s WHERE id = %s"""
            cursor.execute(sql_update_query, (face_id_aws, id_preso))
            conn.commit()
            print(f"face_id_aws atualizado para {face_id_aws} no id_preso {id_preso}")

def atualizar_banco():
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(f"SELECT id, frontal FROM {database}.presos_preso WHERE face_id_aws IS NULL and frontal is not null;")
            for (id_preso, foto) in cursor:
                print(f"Processando id_procurado {id_preso} com foto {foto}")
                
                caminho_imagem = f'http://82.208.20.155/media/{foto}'
                imagem_bytes = carregar_imagem(caminho_imagem)
                
                if imagem_bytes is not None:
                    _,face_id_aws = adicionar_face(imagem_bytes)
                    atualizar_face_id_aws_no_banco(face_id_aws, id_preso)
                else:
                    print(f"Não foi possível carregar a imagem para o id_procurado {id_preso}")
    return True

atualizar_banco()
