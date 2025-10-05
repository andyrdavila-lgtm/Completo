from flask import Blueprint, render_template
from blueprints.core.auth import permission_required

invoices_bp = Blueprint('invoices', __name__,
                        template_folder='../../templates/invoices',
                        url_prefix='/invoices')

@invoices_bp.route('/')
@permission_required('invoices.view')
def manage_invoices():
    """Muestra la lista de facturas."""
    # La lógica CRUD completa se implementará aquí.
    return render_template('invoices/manage_invoices.html')