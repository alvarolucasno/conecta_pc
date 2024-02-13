import mysql.connector
from datetime import datetime
from PIL import Image
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

# Função para redimensionar e salvar a imagem mantendo o aspect ratio
def redimensionar_imagem(caminho_original, caminho_novo, max_resolution):
    try:
        imagem = Image.open(caminho_original)
        
        # Convertendo para o modo RGB, eliminando informações de transparência
        imagem = imagem.convert("RGB")
        
        width, height = imagem.size
        ratio = min(max_resolution / width, max_resolution / height)
        if ratio < 1:
            size = (int(width * ratio), int(height * ratio))
            imagem_resized = imagem.resize(size, Image.LANCZOS)
            imagem_resized.save(caminho_novo)
            return True
        else:
            imagem.save(caminho_novo)
            return False
    except Exception as e:
        print(f"Erro ao processar a imagem {caminho_original}: {e}")
        return False


# Conectando ao banco de dados e buscando os dados
with mysql.connector.connect(**config) as cnx:
    with cnx.cursor(dictionary=True) as cursor:
        select_query = "SELECT * FROM base_inteligencia.detalhamento_pessoa WHERE id_pessoa = 1459629"
        cursor.execute(select_query)
        rows = cursor.fetchall()

        for row in rows:
            caminho_original = os.path.join(pasta_fotos_antigas, row['caminho_foto'])
            data_cadastro = row['data_cadastro']
            
            caminho_foto_nova = os.path.join(pasta_fotos_novas, str(row['id_pessoa']), f"{data_cadastro.strftime('%Y-%m-%d')}.jpg")
            os.makedirs(os.path.dirname(caminho_foto_nova), exist_ok=True)
            redimensionar_imagem(caminho_original, caminho_foto_nova, 1024)
            
            caminho_avatar_novo = os.path.join(pasta_fotos_novas, str(row['id_pessoa']), f"{data_cadastro.strftime('%Y-%m-%d')}_avatar.jpg")
            os.makedirs(os.path.dirname(caminho_avatar_novo), exist_ok=True)
            redimensionar_imagem(caminho_original, caminho_avatar_novo, 200)

            # Ajuste os caminhos relativos conforme necessário
            foto = os.path.join('fotos_procurados', str(row['id_pessoa']), f"{data_cadastro.strftime('%Y-%m-%d')}.jpg").replace('\\', '/')
            avatar = os.path.join('fotos_procurados', str(row['id_pessoa']), f"{data_cadastro.strftime('%Y-%m-%d')}_avatar.jpg").replace('\\', '/')
            
            # Preparar dados para inserção
            data = (
                foto,
                avatar,
                row['origem_foto'],
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
    
print("Conexão ao banco de dados encerrada e recursos liberados.")
