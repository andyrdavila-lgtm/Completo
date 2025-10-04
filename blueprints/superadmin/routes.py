from flask import Blueprint, render_template, jsonify, request, flash
from models.base import db, Client, User, BusinessType, Role, Permission
from blueprints.core.auth import permission_required

superadmin_bp = Blueprint('superadmin', __name__, template_folder='../../templates/superadmin')

@superadmin_bp.route('/')
@permission_required('superadmin.dashboard.view')
def superadmin():
    return render_template('superadmin.html')

@superadmin_bp.route('/roles')
@permission_required('superadmin.roles.manage')
def manage_roles():
    return render_template('manage_roles.html')

# --- Rutas CRUD para Clientes ---

@superadmin_bp.route('/clients')
@permission_required('superadmin.clients.view')
def manage_clients():
    clients = Client.query.options(db.joinedload(Client.business_type)).order_by(Client.name).all()
    return render_template('manage_clients.html', clients=clients)

@superadmin_bp.route('/clients/create', methods=['GET', 'POST'])
@permission_required('superadmin.clients.create')
def create_client():
    if request.method == 'POST':
        # Lógica para crear el cliente
        name = request.form.get('name')
        email = request.form.get('email')
        # ... (obtener todos los demás campos)

        new_client = Client(
            name=name,
            email=email,
            phone=request.form.get('phone'),
            address=request.form.get('address'),
            business_type_id=request.form.get('business_type_id'),
            is_active=request.form.get('is_active') == '1'
        )
        db.session.add(new_client)
        db.session.commit()
        flash(f'Cliente "{name}" creado exitosamente.', 'success')
        return redirect(url_for('superadmin.manage_clients'))

    business_types = BusinessType.query.all()
    return render_template('create_client.html', business_types=business_types)

@superadmin_bp.route('/clients/<int:client_id>/edit', methods=['GET', 'POST'])
@permission_required('superadmin.clients.edit')
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)
    if request.method == 'POST':
        # Lógica para actualizar el cliente
        client.name = request.form.get('name')
        client.email = request.form.get('email')
        client.phone = request.form.get('phone')
        client.address = request.form.get('address')
        client.business_type_id = request.form.get('business_type_id')
        client.is_active = request.form.get('is_active') == '1'
        db.session.commit()
        flash(f'Cliente "{client.name}" actualizado exitosamente.', 'success')
        return redirect(url_for('superadmin.manage_clients'))

    business_types = BusinessType.query.all()
    return render_template('edit_client.html', client=client, business_types=business_types)

@superadmin_bp.route('/clients/<int:client_id>/delete', methods=['POST'])
@permission_required('superadmin.clients.delete')
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    # Opcional: verificar si el cliente tiene usuarios antes de borrar
    if client.users:
        flash(f'No se puede eliminar el cliente "{client.name}" porque tiene usuarios asociados.', 'danger')
        return redirect(url_for('superadmin.manage_clients'))

    db.session.delete(client)
    db.session.commit()
    flash(f'Cliente "{client.name}" eliminado exitosamente.', 'success')
    return redirect(url_for('superadmin.manage_clients'))


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
    """API para obtener tipos de negocio desde la base de datos"""
    try:
        business_types_query = BusinessType.query.order_by(BusinessType.name).all()
        business_types_data = [
            {'id': bt.id, 'name': bt.name} for bt in business_types_query
        ]

        return jsonify({
            'success': True,
            'data': business_types_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@superadmin_bp.route('/api/superadmin/clients')
@permission_required('superadmin.clients.view')
def api_clients():
    """API para obtener lista de clientes"""
    try:
        # Usamos joinedload para optimizar la consulta y traer el tipo de negocio
        clients = Client.query.options(db.joinedload(Client.business_type)).order_by(Client.name).all()
        clients_data = []

        for client in clients:
            clients_data.append({
                'id': client.id,
                'name': client.name,
                'business_type': client.business_type.name if client.business_type else 'No asignado',
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

# --- API para Roles y Permisos ---

@superadmin_bp.route('/api/superadmin/roles', methods=['GET'])
@permission_required('superadmin.roles.manage')
def api_get_roles():
    """Obtiene todos los roles del sistema."""
    roles = Role.query.order_by(Role.name).all()
    return jsonify({'success': True, 'data': [{'id': r.id, 'name': r.name, 'description': r.description} for r in roles]})

@superadmin_bp.route('/api/superadmin/roles', methods=['POST'])
@permission_required('superadmin.roles.manage')
def api_create_role():
    """Crea un nuevo rol."""
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'success': False, 'error': 'El nombre es requerido'}), 400

    if Role.query.filter_by(name=data['name']).first():
        return jsonify({'success': False, 'error': 'Ya existe un rol con este nombre'}), 409

    new_role = Role(name=data['name'], description=data.get('description', ''))
    db.session.add(new_role)
    db.session.commit()

    return jsonify({'success': True, 'data': {'id': new_role.id, 'name': new_role.name, 'description': new_role.description}}), 201

@superadmin_bp.route('/api/superadmin/permissions', methods=['GET'])
@permission_required('superadmin.roles.manage')
def api_get_permissions():
    """Obtiene todos los permisos disponibles."""
    permissions = Permission.query.order_by(Permission.name).all()
    return jsonify({'success': True, 'data': [{'id': p.id, 'name': p.name, 'description': p.description} for p in permissions]})

@superadmin_bp.route('/api/superadmin/roles/<int:role_id>/permissions', methods=['GET'])
@permission_required('superadmin.roles.manage')
def api_get_role_permissions(role_id):
    """Obtiene los permisos de un rol específico."""
    role = Role.query.get_or_404(role_id)
    permission_ids = {p.id for p in role.permissions}
    return jsonify({'success': True, 'data': list(permission_ids)})

@superadmin_bp.route('/api/superadmin/roles/<int:role_id>/permissions', methods=['POST'])
@permission_required('superadmin.roles.manage')
def api_update_role_permissions(role_id):
    """Actualiza los permisos para un rol específico."""
    role = Role.query.get_or_404(role_id)
    data = request.get_json()
    permission_ids = data.get('permission_ids', [])

    # Filtra solo los permisos que realmente existen para evitar errores
    permissions = Permission.query.filter(Permission.id.in_(permission_ids)).all()
    role.permissions = permissions

    db.session.commit()
    return jsonify({'success': True, 'message': f'Permisos para el rol {role.name} actualizados.'})