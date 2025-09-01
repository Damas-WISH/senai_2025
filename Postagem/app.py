# -*- coding: utf-8 -*-

# Passo 1: Importações e Configuração
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Inicializa a aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'somos_todos_sap'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_app.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Postagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Postagem {self.titulo}>'

# --- Rotas da Aplicação ---

# Rota principal que exibe o formulário e a lista de usuários
@app.route('/')
def index():
    postagens = Postagem.query.all()
    return render_template('index.html', postagens=postagens)


@app.route('/adicionar', methods=['POST'])
def adicionar_postagem():
    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')

    
    nova_postagem = Postagem(titulo=titulo, descricao=descricao)
    db.session.add(nova_postagem)
    db.session.commit()

    return redirect(url_for('index'))




# Passo 3: Criando o Banco de Dados Físico
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    # Inicia o servidor de desenvolvimento do Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
