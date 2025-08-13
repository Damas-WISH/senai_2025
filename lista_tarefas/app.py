from flask import Flask, render_template, request

app = Flask(__name__)

# Lista para armazenar as tarefas em memória
tarefas = []

@app.route("/", methods=["GET", "POST"])
def index():
    # Página inicial: só mostra o formulário e a lista
    return render_template("index.html", tarefas=tarefas)

@app.route("/adicionar", methods=["POST"])
def adicionar():
    tarefa = request.form.get("tarefa")
    data_limite = request.form.get("data_limite")

    # Adiciona na lista antes de ir para a página de sucesso
    tarefas.append({"tarefa": tarefa, "data_limite": data_limite})

    # Vai para a página de sucesso
    return render_template("sucesso.html", tarefa=tarefa, data_limite=data_limite)

if __name__ == "__main__":
    app.run(debug=True)
