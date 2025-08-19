from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tarefas = []

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", tarefas=tarefas)

@app.route("/adicionar", methods=["POST"])
def adicionar():
    tarefa = request.form.get("tarefa")
    data_limite = request.form.get("data_limite")
    tarefas.append({"tarefa": tarefa, "data_limite": data_limite})
    return render_template("sucesso.html", tarefa=tarefa, data_limite=data_limite)

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if request.method == "POST":
        tarefas[id]["tarefa"] = request.form["tarefa"]
        tarefas[id]["data_limite"] = request.form["data_limite"]
        return redirect(url_for("index"))

    return render_template("editar.html", tarefa=tarefas[id], id=id)

@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    # Remove a tarefa da lista
    del tarefas[id]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
