from datetime import date
import os
from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, ValidationError
from wtforms.validators import DataRequired

# --- Configuração da Aplicação Flask ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# --- Definição do Formulário ---
class EventoForm(FlaskForm):
    organizador = StringField(
        'Organizador',
        validators=[DataRequired(message="Campo obrigatório!")]
    )
    nome = StringField('Nome')
    data_evento = DateField(
        'Data do Evento',
        format='%Y-%m-%d',
        validators=[
            DataRequired(message="Campo obrigatório!")    
        ]
    )
    mensagem = TextAreaField('Mensagem...')
    enviar = SubmitField("Enviar")

    # ✅ Validador personalizado
    def validate_data_evento(self, field):
        if field.data and field.data < date.today():
            raise ValidationError("A data do evento não pode estar no passado.")

# --- Definição objeto para simulação ---
class Usuario:
    def __init__(self, nome, email, mensagem=""):
        self.nome = nome
        self.email = email
        self.mensagem = mensagem

# --- Rotas da Aplicação ---
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/vazio", methods=['GET', 'POST'])
def formulario_vazio():
    form = EventoForm()
    
    if form.validate_on_submit():
        nome_usuario = form.nome.data
        return render_template('sucesso.html', nome_usuario=nome_usuario)
    
    return render_template('formulario.html', form=form, title="1. Formulário Vazio")

@app.route("/via-argumentos", methods=['GET', 'POST'])
def formulario_via_argumentos():
    form = EventoForm()
    
    if form.validate_on_submit():
        nome_usuario = form.nome.data
        return render_template('sucesso.html', nome_usuario=nome_usuario)
    
    elif not form.is_submitted():
        dados_iniciais = {
            'nome': 'João da Silva',
            'email': 'joao.silva@provedor.com',
            'mensagem': 'Esta é uma mensagem preenchida por argumento.'
        }
        form = EventoForm(**dados_iniciais)
    
    return render_template('formulario.html', form=form, title="2. Formulário preenchido por argumentos")

@app.route("/via-objeto", methods=['GET', 'POST'])
def formulario_via_objeto():
    form = EventoForm()
    
    if form.validate_on_submit():
        nome_usuario = form.nome.data
        return render_template('sucesso.html', nome_usuario=nome_usuario)
    
    elif not form.is_submitted():
        usuario_mock = Usuario(
            nome="Maria Oliveira",
            email="maria.oliveira@provedor.com",
            mensagem="Mensagem vindo via objeto"
        )
        form = EventoForm(obj=usuario_mock)
    
    return render_template('formulario.html', form=form, title="3. Formulário preenchido por objeto.")

# --- Execução da Aplicação ---
if __name__ == '__main__':
    app.run(debug=True)
