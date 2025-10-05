from flask import Blueprint, render_template
from blueprints.core.auth import permission_required

reports_bp = Blueprint('reports', __name__,
                       template_folder='../../templates/reports',
                       url_prefix='/reports')

@reports_bp.route('/')
@permission_required('reports.view')
def reports():
    """Muestra la página principal de informes."""
    # La lógica de los informes se implementará aquí.
    return render_template('reports/reports.html')