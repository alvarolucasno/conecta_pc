import mysql.connector

DB_CONFIG = {
    'host': '38.242.248.229',
    'user': 'alvaro',
    'password': '33441065',
    'database': 'mandados_bnmp'
}

def get_mandados():
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            query = '''
                SELECT
                    mandados_bnmp.pessoas.id_pessoa AS id_pessoa,
                    COALESCE(conecta_pc.mandados_procurados.nome_completo, mandados_bnmp.pessoas.outrosNomes) AS nome,
                    COALESCE(conecta_pc.mandados_procurados.mae, mandados_bnmp.pessoas.nomeMae) AS nomeMae,
                    COALESCE(conecta_pc.mandados_procurados.pai, mandados_bnmp.pessoas.nomePai) AS nomePai,
                    COALESCE(conecta_pc.mandados_procurados.rg, mandados_bnmp.pessoas.rg) AS rg,
                    COALESCE(conecta_pc.mandados_procurados.cpf, mandados_bnmp.pessoas.cpf) AS cpf,
                    CASE 
                        WHEN mandados_bnmp.pessoas.sexo = 'Masculino' THEN 'M'
                        WHEN mandados_bnmp.pessoas.sexo = 'Feminino' THEN 'F'
                    END AS sexo,
                    COALESCE(DATE_FORMAT(conecta_pc.mandados_procurados.data_nascimento, '%d/%m/%Y'), mandados_bnmp.pessoas.dataNascimento) AS dataNascimento,
                    MAX(mandados_bnmp.documentos.dataExpedicao) AS dataExpedicao,
                    IF(conecta_pc.mandados_procurados.id_procurado_bnmp IS NOT NULL, 1, 0) AS dado_detalhado,
                    conecta_pc.mandados_procurados.avatar
                FROM mandados_bnmp.pessoas
                LEFT JOIN mandados_bnmp.documentos
                    ON mandados_bnmp.pessoas.id_pessoa = mandados_bnmp.documentos.id_pessoa
                LEFT JOIN mandados_bnmp.orgaoUsuarioCriador
                    ON mandados_bnmp.documentos.id_orgaoUsuarioCriador = mandados_bnmp.orgaoUsuarioCriador.id_orgaoUsuarioCriador
                LEFT JOIN mandados_bnmp.enderecos_pessoas
                    ON mandados_bnmp.pessoas.id_pessoa = mandados_bnmp.enderecos_pessoas.id_pessoa
                LEFT JOIN conecta_pc.mandados_procurados
                    ON mandados_bnmp.pessoas.id_pessoa = conecta_pc.mandados_procurados.id_procurado_bnmp
                WHERE mandados_bnmp.documentos.valido = 1
                AND (mandados_bnmp.orgaoUsuarioCriador.uf = "Sergipe" or mandados_bnmp.enderecos_pessoas.uf = "Sergipe")
                GROUP BY mandados_bnmp.pessoas.id_pessoa
                ORDER BY MAX(mandados_bnmp.documentos.dataExpedicao) DESC;
            '''
            cursor.execute(query)
            colunas = [i[0] for i in cursor.description]
            dados = [dict(zip(colunas, row)) for row in cursor.fetchall()]
            
            return dados
        
def get_name_by_id(id):
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            query = '''
            SELECT DISTINCT
                id_pessoa,
                outrosNomes as nome_pesssoa
            FROM mandados_bnmp.alvos_mandados_sergipe
            WHERE id_pessoa = %s;
            '''
            cursor.execute(query, (id,))
            dados_alvo = cursor.fetchone()
            
            return dados_alvo

def save_dados_alvo(id_pessoa, nome, dataNascimento, mae, pai, rg, uf_rg, cpf, cnh, nis, sap, caminho_foto, origem_foto, id_cadastrador, nome_cadastrador, cpf_cadastrador, data_cadastro, morto, observacao):
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            query = """
            INSERT INTO base_inteligencia.detalhamento_pessoa 
            (id_pessoa, nome, dataNascimento, mae, pai, rg, uf_rg, cpf, cnh, nis, sap, caminho_foto, origem_foto, id_cadastrador, nome_cadastrador, cpf_cadastrador, data_cadastro, morto, observacao)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                nome = VALUES(nome),
                dataNascimento = VALUES(dataNascimento),
                mae = VALUES(mae),
                pai = VALUES(pai),
                rg = VALUES(rg),
                uf_rg = VALUES(uf_rg),
                cpf = VALUES(cpf),
                cnh = VALUES(cnh),
                nis = VALUES(nis),
                sap = VALUES(sap),
                caminho_foto = VALUES(caminho_foto),
                origem_foto = VALUES(origem_foto),
                id_cadastrador = VALUES(id_cadastrador),
                nome_cadastrador = VALUES(nome_cadastrador),
                cpf_cadastrador = VALUES(cpf_cadastrador),
                data_cadastro = VALUES(data_cadastro),
                morto = VALUES(morto),
                observacao = VALUES(observacao)
            """
            # Dados para inserção/atualização
            data = (id_pessoa, nome, dataNascimento, mae, pai, rg, uf_rg, cpf, cnh, nis, sap, caminho_foto, origem_foto, id_cadastrador, nome_cadastrador, cpf_cadastrador, data_cadastro, morto, observacao)
            cursor.execute(query, data)
            conn.commit()
