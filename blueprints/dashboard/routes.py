from flask import Blueprint, render_template, session, g

# Definir el blueprint aquí mismo
dashboard_bp = Blueprint('dashboard', __name__, template_folder='../../templates/dashboard')

@dashboard_bp.route('/')
def dashboard():
    """Página principal del dashboard"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = g.user
    return render_template('dashboard.html', user=user)

# No necesitas importar dashboard_bp desde __init__.py