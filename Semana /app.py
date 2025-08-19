# Importa as classes e funções necessárias
from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

# 1. CONFIGURAÇÃO DA APLICAÇÃO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-dificil-de-adivinhar'

# 2. FORMULÁRIOS
class MeuFormulario(FlaskForm):
    """Formulário de contato simples"""
    nome = StringField('Nome Completo', validators=[DataRequired(message="Este campo é obrigatório.")])
    email = StringField('Seu Melhor E-mail', validators=[
        DataRequired(message="Este campo é obrigatório."),
        Email(message="Por favor, insira um e-mail válido.")
    ])
    submit = SubmitField('Enviar Cadastro')


class FormularioRegistro(FlaskForm):
    """Formulário de Registro de Usuário"""
    nome = StringField('Nome Completo', validators=[DataRequired(message="Obrigatório.")])
    email = StringField('E-mail', validators=[
        DataRequired(message="Obrigatório."),
        Email(message="Formato de e-mail inválido.")
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message="Obrigatório."),
        Length(min=8, message="A senha deve ter no mínimo 8 caracteres.")
    ])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[
        DataRequired(message="Obrigatório."),
        EqualTo('senha', message="As senhas devem ser iguais.")
    ])
    biografia = TextAreaField('Biografia (opcional)')
    aceitar_termos = BooleanField('Aceito os Termos de Serviço', validators=[
        DataRequired(message="Você deve aceitar os termos.")
    ])
    submit = SubmitField('Registrar')


# 3. ROTAS EXISTENTES
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = MeuFormulario()
    if form.validate_on_submit():
        nome_usuario = form.nome.data
        email_usuario = form.email.data
        flash(f'Cadastro recebido com sucesso para {nome_usuario} ({email_usuario})!', 'success')
        return redirect(url_for('formulario'))
    return render_template('formulario.html', form=form)


@app.route('/formulario/preenchido-args', methods=['GET', 'POST'])
def formulario_com_argumentos():
    form = MeuFormulario(nome="Fulano de Tal", email="fulano@exemplo.com")
    if form.validate_on_submit():
        flash(f'Dados de "{form.nome.data}" atualizados com sucesso!', 'success')
        return redirect(url_for('formulario_com_argumentos'))
    return render_template('formulario.html', form=form)


@app.route('/formulario/preenchido-obj', methods=['GET', 'POST'])
def formulario_com_objeto():
    class UsuarioMock:
        def __init__(self, nome, email):
            self.nome = nome
            self.email = email
    usuario_do_banco = UsuarioMock(nome="Ciclano da Silva", email="ciclano@banco.com")
    form = MeuFormulario(obj=usuario_do_banco)
    if form.validate_on_submit():
        flash(f'Dados de "{form.nome.data}" atualizados com sucesso!', 'success')
        return redirect(url_for('formulario_com_objeto'))
    return render_template('formulario.html', form=form)


# 🔹 NOVA ROTA DE REGISTRO
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = FormularioRegistro()
    if form.validate_on_submit():
        nome = form.nome.data
        bio = form.biografia.data
        if bio:
            flash(f'Bem-vindo, {nome}! Sua biografia: "{bio[:50]}..."', 'success')
        else:
            flash(f'Bem-vindo, {nome}! Registro realizado com sucesso!', 'success')
        return redirect(url_for('registro'))
    return render_template('registro.html', form=form)


# Rota principal
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
