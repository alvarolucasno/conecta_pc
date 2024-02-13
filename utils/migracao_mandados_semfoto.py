import mysql.connector
from datetime import datetime
import os

config = {
    'host': '38.242.248.229',
    'user': 'alvaro',
    'password': '33441065',
    'database': 'conecta_pc_desenvolvimento',
    'raise_on_warnings': True,
}

pasta_fotos_antigas = r'C:\Users\ALVAR\Desktop'
pasta_fotos_novas = r'C:\Users\ALVAR\Desktop\fotos_procurados'

# Conectando ao banco de dados e buscando os dados
with mysql.connector.connect(**config) as cnx:
    with cnx.cursor(dictionary=True) as cursor:
        select_query = "SELECT * FROM base_inteligencia.detalhamento_pessoa WHERE (caminho_foto IS NULL OR caminho_foto = '')"
        cursor.execute(select_query)
        rows = cursor.fetchall()

        for row in rows:
            # Printando o registro sem foto e origem_foto
            print("Registro sem foto e origem_foto:", row)
            
            data = (
                None,  # foto
                None,  # avatar
                None,  # origem_foto
                row['id_pessoa'],
                row['nome'],
                row['dataNascimento'],
                row['mae'],
                row['pai'],
                row['rg'],
                row['uf_rg'], 
                row['cpf'],
                row['cnh'], 
                row['nis'], 
                row['sap'],
                "M",
                row['morto'],
                row['observacao'],
                row['cpf_cadastrador'],
                row['nome_cadastrador'],
                datetime.now(),
                datetime.now(),
                1,
                1,
                1
            )
            
            with cnx.cursor() as insert_cursor:
                insert_query = """
                INSERT INTO mandados_procurados 
                (foto, avatar, origem_foto, id_procurado_bnmp, nome_completo, data_nascimento, mae, pai, rg, uf_rg, cpf, cnh, nis, sap, sexo, informacao_morte, observacao, cpf_cadastrador, nome_cadastrador, created_at, updated_at, ativo, created_by_id, updated_by_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                insert_cursor.execute(insert_query, data)
                cnx.commit()
                
                # Printando o registro salvo
                print("Registro salvo:", row)

print("Conexão ao banco de dados encerrada e recursos liberados.")
