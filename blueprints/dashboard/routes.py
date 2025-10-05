from flask import Blueprint, render_template
from blueprints.core.auth import permission_required

dashboard_bp = Blueprint('dashboard', __name__,
                         template_folder='../../templates/dashboard',
                         url_prefix='/dashboard')

@dashboard_bp.route('/')
@permission_required('dashboard.view')
def dashboard():
    """Muestra el dashboard principal del cliente."""
    return render_template('dashboard.html')