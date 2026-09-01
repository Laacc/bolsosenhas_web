import os
import random
import sqlite3
import string
import subprocess

class GerenciadorSenhas:
    def __init__(self, caminho):
        self.caminho = caminho
        diretorio = os.path.dirname(self.caminho)
        if diretorio:
            os.makedirs(diretorio, exist_ok=True)
        with sqlite3.connect(self.caminho) as con:
            cursor = con.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS data (" \
            "id INTEGER PRIMARY KEY," \
            "plataforma TEXT," \
            "senha TEXT)")
            con.commit()

    def gerar_senha(self, tamanho=14):
        caracteres = string.ascii_letters + string.digits + string.punctuation
        senha = "".join(random.choices(caracteres, k=tamanho))
        return senha

    def inserir_senha_db(self, plataforma, senha):
        nova_senha = ((plataforma, senha))
        with sqlite3.connect(self.caminho) as con:
            cursor = con.cursor()
            cursor.execute("INSERT INTO data (plataforma, senha) VALUES (?, ?)", nova_senha)
            con.commit()
    def carregar_senhas(self):
        with sqlite3.connect(self.caminho) as con:
            senhas = []
            cursor = con.cursor()
            cursor.execute("SELECT * FROM data ORDER BY id")
            fetch = cursor.fetchall()
            for linha in fetch:
                senhas.append(linha)
            return senhas

    def trocar_senha(self, plataforma):
        senha = self.gerar_senha()
        nova_senha = ((senha, plataforma))
        with sqlite3.connect(self.caminho) as con:
            cursor = con.cursor()
            cursor.execute("UPDATE data SET senha=(?) WHERE plataforma=(?)", nova_senha)
            row_bool = cursor.rowcount
            con.commit()
            return row_bool == 1

    def deletar_senha(self, plataforma):
        plataforma_busca = ((plataforma,))
        with sqlite3.connect(self.caminho) as con:
            cursor = con.cursor()
            cursor.execute("DELETE FROM data WHERE plataforma=(?)", plataforma_busca)
            row_bool = cursor.rowcount
            con.commit()
            return row_bool == 1

    def copiar_senha(self, senha):
        subprocess.run("clip", input=senha, check=True, encoding="utf-8")
        

