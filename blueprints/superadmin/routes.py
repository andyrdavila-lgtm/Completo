from flask import Blueprint, render_template
from blueprints.core.auth import permission_required

superadmin_bp = Blueprint('superadmin', __name__,
                          template_folder='../../templates/superadmin',
                          url_prefix='/superadmin')

@superadmin_bp.route('/')
@permission_required('superadmin.dashboard.view')
def superadmin():
    """Muestra el dashboard principal del superadministrador."""
    return render_template('superadmin/dashboard.html')

# Aquí se añadirán las rutas para gestionar clientes, roles, etc.