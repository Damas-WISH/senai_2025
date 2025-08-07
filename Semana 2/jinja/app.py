from flask import Flask, render_template

app = Flask (__name__)

@app.route('/')
def index():
    usuario = 'Nicolas Damas Wischral'
    return render_template('index.html', nome_usuario = usuario)

@app.route('/perfil/<nome>')
def perfil (nome):
    logado = True
    usuario = nome
    return render_template('perfil.html', logado=logado,nome_usuario = usuario)

@app.route('/lista_produtos')
def lista_produtos():
    produtos = ['cama','coberta','travesseiro']
    return render_template('produtos.html', lista=produtos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)



