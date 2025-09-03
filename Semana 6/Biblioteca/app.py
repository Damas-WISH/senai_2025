# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

# Configuração básica
app = Flask(__name__)
app.config['SECRET_KEY'] = 'minha_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estante.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------ MODELOS ------------------

class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), unique=True, nullable=False)
    livros = db.relationship('Livro', backref='autor', lazy=True)

    def __repr__(self):
        return f'<Autor {self.nome}>'

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    ano_publicacao = db.Column(db.Integer, nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('autor.id'), nullable=False)

    def __repr__(self):
        return f'<Livro {self.titulo}>'

# ------------------ FORMULÁRIOS ------------------

class AutorForm(FlaskForm):
    nome = StringField("Nome do Autor", validators=[DataRequired()])
    submit = SubmitField("Adicionar Autor")

class LivroForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired()])
    ano_publicacao = IntegerField("Ano de Publicação", validators=[DataRequired()])
    autor = QuerySelectField("Autor", query_factory=lambda: Autor.query.all(),
                             get_label="nome", allow_blank=False)
    submit = SubmitField("Adicionar Livro")

# ------------------ ROTAS ------------------

@app.route("/autores", methods=["GET", "POST"])
def autores():
    form = AutorForm()
    if form.validate_on_submit():
        novo_autor = Autor(nome=form.nome.data)
        db.session.add(novo_autor)
        db.session.commit()
        flash("Autor cadastrado com sucesso!", "success")
        return redirect(url_for("autores"))

    lista_autores = Autor.query.all()
    return render_template("autores.html", form=form, autores=lista_autores)


@app.route("/", methods=["GET", "POST"])
@app.route("/livros", methods=["GET", "POST"])
def livros():
    form = LivroForm()
    if form.validate_on_submit():
        novo_livro = Livro(
            titulo=form.titulo.data,
            ano_publicacao=form.ano_publicacao.data,
            autor=form.autor.data
        )
        db.session.add(novo_livro)
        db.session.commit()
        flash("Livro cadastrado com sucesso!", "success")
        return redirect(url_for("livros"))

    lista_livros = Livro.query.all()
    return render_template("livros.html", form=form, livros=lista_livros)

# ------------------ MAIN ------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
