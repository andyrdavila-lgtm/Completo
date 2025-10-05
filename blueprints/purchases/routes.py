from flask import Blueprint, render_template
from blueprints.core.auth import permission_required

purchases_bp = Blueprint('purchases', __name__,
                         template_folder='../../templates/purchases',
                         url_prefix='/purchases')

@purchases_bp.route('/')
@permission_required('purchases.view')
def manage_purchases():
    """Muestra la lista de órdenes de compra."""
    # La lógica CRUD completa se implementará aquí.
    return render_template('purchases/manage_purchases.html')