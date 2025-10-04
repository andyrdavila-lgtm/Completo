from flask import Blueprint, render_template

# Definir el blueprint aquí
users_bp = Blueprint('users', __name__, template_folder='../../templates/users')

@users_bp.route('/')
def users():
    """Gestión de usuarios"""
    return render_template('users.html')