import sys
import os
from dotenv import load_dotenv
from flask import Flask, session, g, redirect, url_for
from flask_migrate import Migrate
import urllib.parse
from datetime import timedelta

# Cargar variables de entorno desde .env
load_dotenv()

# Importar la instancia de la base de datos
from models.base import db

def create_app(config_name='default'):
    """
    Application Factory: Crea y configura la aplicación Flask.
    """
    app = Flask(__name__)

    # --- Configuración ---
    if config_name == 'testing':
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL', 'sqlite:///:memory:')
        app.config['SECRET_KEY'] = 'test-secret-key'
        app.config['WTF_CSRF_ENABLED'] = False
    else:
        # Configuración para producción/desarrollo
        # Priorizar la URI completa si está en el entorno, si no, construirla.
        if 'SQLALCHEMY_DATABASE_URI' in os.environ:
            app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
        else:
            DB_SERVER = os.getenv('DB_SERVER', 'localhost')
            DB_NAME = os.getenv('DB_NAME', 'SISTEMACOM')
            DB_DRIVER = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
            DB_USER = os.getenv('DB_USER')
            DB_PASSWORD = os.getenv('DB_PASSWORD')

            if DB_USER and DB_PASSWORD:
                connection_config = f'DRIVER={{{DB_DRIVER}}};SERVER={DB_SERVER};DATABASE={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD};'
            else:
                connection_config = f'DRIVER={{{DB_DRIVER}}};SERVER={DB_SERVER};DATABASE={DB_NAME};Trusted_Connection=yes;'

            encoded_connection_string = urllib.parse.quote_plus(connection_config)
            app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={encoded_connection_string}"

        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'una-clave-secreta-de-desarrollo-muy-simple')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')

    # --- Inicializar extensiones ---
    db.init_app(app)
    Migrate(app, db)

    # --- Registrar Blueprints ---
    from blueprints.auth.routes import auth_bp
    from blueprints.dashboard.routes import dashboard_bp
    from blueprints.users.routes import users_bp
    from blueprints.clients.routes import clients_bp
    from blueprints.reports.routes import reports_bp
    from blueprints.superadmin.routes import superadmin_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(clients_bp, url_prefix='/clients')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    app.register_blueprint(superadmin_bp, url_prefix='/superadmin')

    # --- Registrar Middleware y Rutas Principales ---
    with app.app_context():
        # Middleware
        @app.before_request
        def before_request():
            from models.base import User, Role
            from sqlalchemy.orm import joinedload

            g.user = None
            g.tenant = None

            if 'user_id' in session:
                user = db.session.query(User).options(
                    joinedload(User.roles).joinedload(Role.permissions)
                ).get(session['user_id'])
                g.user = user
                if g.user:
                    g.tenant = g.user.client if g.user.role != 'superadmin' else None

        @app.route('/')
        def index():
            if 'user_id' in session:
                return redirect(url_for('superadmin.superadmin' if g.user and g.user.role == 'superadmin' else 'dashboard.dashboard'))
            return redirect(url_for('auth.login'))

        # Comando para inicializar la base de datos
        @app.cli.command("init-db")
        def init_db_command():
            """Inicializar la base de datos con datos iniciales."""
            from utils.initialization import initialize_system_data, create_demo_users
            print("🗃️ Creando todas las tablas...")
            db.create_all()
            print("✅ Tablas creadas.")
            initialize_system_data()
            create_demo_users()
            print("🎉 Sistema inicializado correctamente.")

    return app

if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*60)
    print("🚀 SISTEMA SISTEMACOM INICIADO")
    print("="*60)
    print(f"🔧 Modo DEBUG: {app.config['DEBUG']}")
    print("📍 Servidor ejecutándose en: http://localhost:8000")
    print("🔑 Para inicializar la base de datos, ejecuta: flask init-db")
    print("="*60)
    app.run(debug=app.config['DEBUG'], port=8000, host='0.0.0.0')