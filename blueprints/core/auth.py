from functools import wraps
from flask import g, flash, redirect, url_for

def permission_required(permission_name):
    """
    Decorador que comprueba si el usuario actual tiene el permiso especificado.
    Si no está autenticado, redirige al login.
    Si no tiene permiso, muestra un error 403 (Prohibido).
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.user:
                flash('Debes iniciar sesión para ver esta página.', 'warning')
                return redirect(url_for('auth.login'))

            if not g.user.has_permission(permission_name):
                # Idealmente, aquí se mostraría una página de error 403.
                # Por ahora, redirigimos al dashboard con un mensaje de error.
                flash('No tienes permiso para acceder a esta página.', 'danger')
                return redirect(url_for('dashboard.dashboard'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator