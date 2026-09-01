from flask import Flask, render_template, redirect, url_for, request
from manager import GerenciadorSenhas

app = Flask(__name__)
gerenciador = GerenciadorSenhas("data/senhas.db")


@app.route("/")
def pagina_inicial():
    return render_template("index.html")

@app.route("/gerar", methods=['GET', 'POST'])
def pagina_gerar_senha():
    if request.method == 'POST':
        plataforma = request.form.get('plataforma')
        senha = gerenciador.gerar_senha()
        gerenciador.inserir_senha_db(plataforma, senha)
        return redirect(url_for('pagina_consultar_senhas'))
    else:
        return render_template("gerar_senha.html")

@app.route("/consultar")
def pagina_consultar_senhas():
    lista_senhas = gerenciador.carregar_senhas()
    return render_template("consultar_senhas.html", senhas=lista_senhas)

@app.route("/deletar", methods=['POST'])
def deletar_senha():
        plataforma = request.form.get('plataforma')
        gerenciador.deletar_senha(plataforma)
        return redirect(url_for('pagina_consultar_senhas'))

@app.route("/trocar", methods=['POST'])
def trocar_senha():
     plataforma = request.form.get('plataforma')
     gerenciador.trocar_senha(plataforma)
     return redirect(url_for('pagina_consultar_senhas'))

@app.route("/copiar", methods=['POST'])
def copiar_senha():
     senha = request.form.get('senha')
     gerenciador.copiar_senha(senha)
     return redirect(url_for('pagina_consultar_senhas'))


if __name__ == "__main__":
    app.run(debug=True)