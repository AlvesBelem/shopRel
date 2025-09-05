import psycopg2
import pandas as pd
import json
import os


class Database:
    def __init__(self):
        try:
            # Caminho para o JSON de configuração
            config_path = os.path.join(os.path.dirname(__file__), '../config/db_config.json')

            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # Conexão com o PostgreSQL usando psycopg2
            self.conn = psycopg2.connect(
                host=config['server'],
                database=config['database'],
                user=config['username'],
                password=config['password']
            )

        except Exception as e:
            raise Exception(f"Erro ao conectar ao banco de dados: {e}")

    def query(self, sql, params=None):
        """
        Executa uma consulta SQL e retorna os resultados como DataFrame.
        """
        try:
            return pd.read_sql_query(sql, self.conn, params=params)
        except Exception as e:
            raise Exception(f"Erro ao executar a consulta: {e}")
