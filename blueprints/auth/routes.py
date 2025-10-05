from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.base import db, User
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__, template_folder='../../templates/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            if not user.is_active:
                flash('Tu cuenta está desactivada.', 'danger')
                return redirect(url_for('auth.login'))

            session['user_id'] = user.id
            session.permanent = True
            flash('Login exitoso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'error')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('auth.login'))