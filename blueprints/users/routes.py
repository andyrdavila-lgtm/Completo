from flask import Blueprint, render_template, request, flash, redirect, url_for, g
from models.base import db, User, Role
from blueprints.core.auth import permission_required

# Definir el blueprint aquí
users_bp = Blueprint('users', __name__, template_folder='../../templates/users')

@users_bp.route('/')
@permission_required('users.view')
def manage_users():
    """Muestra la lista de usuarios para el cliente actual."""
    if not g.tenant:
        flash('No tienes un cliente asignado.', 'danger')
        return redirect(url_for('dashboard.dashboard'))

    # Cargar usuarios con sus roles para optimizar
    users = User.query.filter_by(client_id=g.tenant.id).options(db.joinedload(User.roles)).all()
    return render_template('manage_users.html', users=users)

@users_bp.route('/create', methods=['GET', 'POST'])
@permission_required('users.create')
def create_user():
    """Crea un nuevo usuario para el cliente actual."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validaciones
        if not all([username, email, password]):
            flash('Todos los campos son requeridos.', 'danger')
            return render_template('create_user.html')

        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe.', 'danger')
            return render_template('create_user.html')

        new_user = User(
            username=username,
            email=email,
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            client_id=g.tenant.id,
            is_active=request.form.get('is_active') == '1'
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash(f'Usuario "{username}" creado exitosamente.', 'success')
        return redirect(url_for('users.manage_users'))

    return render_template('create_user.html')

@users_bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@permission_required('users.edit')
def edit_user(user_id):
    """Edita un usuario existente del cliente actual."""
    user_to_edit = User.query.filter_by(id=user_id, client_id=g.tenant.id).first_or_404()

    if request.method == 'POST':
        user_to_edit.email = request.form.get('email')
        user_to_edit.first_name = request.form.get('first_name')
        user_to_edit.last_name = request.form.get('last_name')
        user_to_edit.is_active = request.form.get('is_active') == '1'

        password = request.form.get('password')
        if password:
            user_to_edit.set_password(password)

        db.session.commit()
        flash(f'Usuario "{user_to_edit.username}" actualizado exitosamente.', 'success')
        return redirect(url_for('users.manage_users'))

    return render_template('edit_user.html', user=user_to_edit)

@users_bp.route('/<int:user_id>/roles', methods=['GET', 'POST'])
@permission_required('users.edit') # Usamos el mismo permiso que para editar
def manage_user_roles(user_id):
    """Gestiona los roles de un usuario específico."""
    user_to_manage = User.query.filter_by(id=user_id, client_id=g.tenant.id).first_or_404()

    if request.method == 'POST':
        role_ids = request.form.getlist('roles')
        # Asignar los nuevos roles
        user_to_manage.roles = Role.query.filter(Role.id.in_(role_ids)).all()
        db.session.commit()
        flash(f'Roles para "{user_to_manage.username}" actualizados.', 'success')
        return redirect(url_for('users.manage_users'))

    all_roles = Role.query.order_by(Role.name).all()
    return render_template('manage_user_roles.html', user_to_manage=user_to_manage, all_roles=all_roles)