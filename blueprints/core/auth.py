from functools import wraps
from flask import g, flash, redirect, url_for

def permission_required(permission_name):
    """
    Decorador que comprueba si el usuario actual tiene el permiso especificado.
    Redirige a la página de login si no está autenticado, o al dashboard
    si no tiene permisos suficientes.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Si el usuario no está logueado, g.user no existirá.
            if not hasattr(g, 'user') or not g.user:
                flash('Debes iniciar sesión para ver esta página.', 'warning')
                return redirect(url_for('auth.login'))

            # Comprobar si el usuario tiene el permiso requerido.
            if not g.user.has_permission(permission_name):
                flash('No tienes permiso para acceder a esta página.', 'danger')
                # Redirigir al dashboard como página por defecto si no hay permiso.
                return redirect(url_for('dashboard.dashboard'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator