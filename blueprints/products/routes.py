from flask import Blueprint, render_template
from blueprints.core.auth import permission_required

products_bp = Blueprint('products', __name__,
                        template_folder='../../templates/products',
                        url_prefix='/products')

@products_bp.route('/')
@permission_required('products.view')
def manage_products():
    """Muestra la lista de productos del cliente."""
    # La lógica CRUD completa se implementará aquí.
    return render_template('products/manage_products.html')