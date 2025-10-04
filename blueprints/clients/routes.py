from flask import Blueprint, render_template

clients_bp = Blueprint('clients', __name__, template_folder='../../templates')

@clients_bp.route('/')
def clients():
    return render_template('clientes.html')