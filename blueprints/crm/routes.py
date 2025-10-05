from flask import Blueprint, render_template
from blueprints.core.auth import permission_required

crm_bp = Blueprint('crm', __name__,
                   template_folder='../../templates/crm',
                   url_prefix='/crm')

@crm_bp.route('/')
@permission_required('crm.view')
def manage_crm():
    """Muestra la página principal de CRM."""
    # La lógica CRUD completa se implementará aquí.
    return render_template('crm/manage_crm.html')