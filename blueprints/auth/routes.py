from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.base import db, User
from werkzeug.security import check_password_hash
from flask import current_app

# Definir el blueprint
auth_bp = Blueprint('auth', __name__, template_folder='../../templates/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    # Si ya está logueado, redirigir al dashboard
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
        if user:
            if user.role == 'superadmin':
                return redirect(url_for('superadmin.superadmin'))
            else:
                return redirect(url_for('dashboard.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session.permanent = True
            flash('Login exitoso!', 'success')
            
            if user.role == 'superadmin':
                return redirect(url_for('superadmin.superadmin'))
            else:
                return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('auth.login'))