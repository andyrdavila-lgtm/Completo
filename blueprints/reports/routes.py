from flask import Blueprint, render_template, g, flash, redirect, url_for
from models.base import User
from blueprints.core.auth import permission_required

reports_bp = Blueprint('reports', __name__, template_folder='../../templates/reports')

@reports_bp.route('/')
@permission_required('reports.view')
def reports():
    """Muestra la página de informes para el cliente actual."""
    if not g.tenant:
        flash('No tienes un cliente asignado para ver informes.', 'danger')
        return redirect(url_for('dashboard.dashboard'))

    # Calcular estadísticas de usuarios para el cliente actual
    total_users = User.query.filter_by(client_id=g.tenant.id).count()
    active_users = User.query.filter_by(client_id=g.tenant.id, is_active=True).count()

    user_stats = {
        'total_users': total_users,
        'active_users': active_users,
        'inactive_users': total_users - active_users
    }

    return render_template('reports.html', user_stats=user_stats)