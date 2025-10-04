from functools import wraps
from flask import session, redirect, url_for, flash
from models.base import User, UserModule

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor inicia sesión para acceder a esta página.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def get_user_modules(user_id, client_id):
    """Obtener módulos asignados a un usuario"""
    try:
        user_modules = UserModule.query.filter_by(user_id=user_id).all()
        modules = []
        for um in user_modules:
            if um.module and um.can_view:
                modules.append({
                    'id': um.module.id,
                    'name': um.module.name,
                    'display_name': um.module.display_name,
                    'route': um.module.route,
                    'icon': um.module.icon,
                    'can_view': um.can_view,
                    'can_edit': um.can_edit,
                    'can_delete': um.can_delete,
                    'can_manage': um.can_manage
                })
        return modules
    except Exception as e:
        print(f"Error obteniendo módulos del usuario: {e}")
        return []