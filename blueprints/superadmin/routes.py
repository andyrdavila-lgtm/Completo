from flask import Blueprint, render_template, jsonify
from models.base import db, Client, User

superadmin_bp = Blueprint('superadmin', __name__, template_folder='../../templates/superadmin')

@superadmin_bp.route('/')
def superadmin():
    return render_template('superadmin.html')

# --- API Routes ---
@superadmin_bp.route('/api/superadmin/stats')
def api_stats():
    """API para obtener estadísticas del sistema"""
    try:
        total_clients = Client.query.count()
        total_users = User.query.count()
        active_clients = Client.query.filter_by(is_active=True).count()
        
        return jsonify({
            'success': True,
            'data': {
                'total_clients': total_clients,
                'total_users': total_users,
                'active_clients': active_clients
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@superadmin_bp.route('/api/superadmin/business-types')
def api_business_types():
    """API para obtener tipos de negocio"""
    try:
        # Esto es un ejemplo - ajusta según tu modelo de datos
        business_types = [
            {'id': 1, 'name': 'Restaurante'},
            {'id': 2, 'name': 'Cafetería'},
            {'id': 3, 'name': 'Bar'},
            {'id': 4, 'name': 'Hotel'},
            {'id': 5, 'name': 'Tienda'},
        ]
        
        return jsonify({
            'success': True,
            'data': business_types
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@superadmin_bp.route('/api/superadmin/clients')
def api_clients():
    """API para obtener lista de clientes"""
    try:
        clients = Client.query.all()
        clients_data = []
        
        for client in clients:
            clients_data.append({
                'id': client.id,
                'name': client.name,
                'business_type': client.business_type,
                'is_active': client.is_active,
                'created_at': client.created_at.isoformat() if client.created_at else None
            })
        
        return jsonify({
            'success': True,
            'data': clients_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500