import psycopg2
import pandas as pd
import json
import os

class DBConnection:
    def __init__(self):
        self.conn = None
        self.load_config()

    def load_config(self):
        try:
            with open("config/db_config.json", "r") as f:
                config = json.load(f)
            self.host = config["host"]
            self.database = config["database"]
            self.user = config["user"]
            self.password = config["password"]
        except Exception as e:
            raise Exception(f"Erro ao carregar configurações do banco: {e}")

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
        except Exception as e:
            raise Exception(f"Erro ao conectar ao banco de dados: {e}")

    def query(self, sql, params=None):
        try:
            if self.conn is None:
                self.connect()

            if self.conn is None:
                raise Exception("Conexão com o banco de dados não foi estabelecida.")

            with self.conn.cursor() as cur:
                cur.execute(sql, params)
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                df = pd.DataFrame(rows, columns=columns)
                return df

        except Exception as e:
            raise Exception(f"Erro ao executar consulta: {e}")

            

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
