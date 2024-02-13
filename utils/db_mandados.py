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
                    IFNULL(d.id_procurado_bnmp, m.id_pessoa) AS id_pessoa,
                    IFNULL(d.nome_completo, m.outrosNomes) AS nome,
                    IFNULL(d.mae, m.nomeMae) AS nomeMae,
                    IFNULL(d.pai, m.nomePai) AS nomePai,
                    IFNULL(d.rg, m.rg) AS rg,
                    COALESCE(
                        CASE 
                            WHEN CHAR_LENGTH(d.cpf) = 11 THEN CONCAT(SUBSTRING(d.cpf, 1, 3), '.', SUBSTRING(d.cpf, 4, 3), '.', SUBSTRING(d.cpf, 7, 3), '-', SUBSTRING(d.cpf, 10, 2))
                            ELSE ''
                        END,
                        CASE
                            WHEN CHAR_LENGTH(m.cpf) = 11 THEN CONCAT(SUBSTRING(m.cpf, 1, 3), '.', SUBSTRING(m.cpf, 4, 3), '.', SUBSTRING(m.cpf, 7, 3), '-', SUBSTRING(m.cpf, 10, 2))
                            ELSE ''
                        END,
                        ''
                    ) AS cpf,
                    CASE m.sexo
                        WHEN 'Masculino' THEN 'M'
                        WHEN 'Feminino' THEN 'F'
                    END AS sexo,
                    DATE_FORMAT(IFNULL(d.data_nascimento, m.dataNascimento), '%d/%m/%Y') AS dataNascimento,
                    DATE_FORMAT(m.dataExpedicao, '%d/%m/%Y %H:%i') AS dataExpedicaoFormatada,
                    IF(d.id_procurado_bnmp IS NOT NULL, 1, 0) AS dado_detalhado,
                    d.foto
                FROM 
                    mandados_bnmp.mandados_prisao_criminais_sergipe AS m
                LEFT JOIN conecta_pc_desenvolvimento.mandados_procurados AS d
                    ON m.id_pessoa = d.id_procurado_bnmp
                INNER JOIN (
                    SELECT 
                        id_pessoa,
                        MAX(id_documento) AS id_documentoMaximo
                    FROM 
                        mandados_bnmp.mandados_prisao_criminais_sergipe
                    GROUP BY 
                        id_pessoa
                ) AS subconsulta 
                    ON m.id_pessoa = subconsulta.id_pessoa AND m.id_documento = subconsulta.id_documentoMaximo
                ORDER BY 
                    m.dataExpedicao DESC;
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
            FROM mandados_bnmp.mandados_prisao_criminais_sergipe
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
