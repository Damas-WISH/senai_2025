from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from models.transaction import Transaction

finance_bp = Blueprint("finance", __name__)

@finance_bp.route("/transactions")
@login_required
def transactions():
    transacoes = Transaction.query.filter_by(user_id=current_user.id).all()
    return render_template("transactions.html", transacoes=transacoes)

@finance_bp.route("/add-transaction", methods=["GET", "POST"])
@login_required
def add_transaction():
    if request.method == "POST":
        amount = float(request.form.get("amount"))
        category = request.form.get("category")
        t_type = request.form.get("type")

        new_t = Transaction(
            amount=amount,
            category=category,
            type=t_type,
            user_id=current_user.id
        )

        db.session.add(new_t)
        db.session.commit()

        return redirect(url_for("finance.transactions"))

    return render_template("add_transaction.html")
