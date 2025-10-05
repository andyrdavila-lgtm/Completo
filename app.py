import os
from flask import Flask, redirect, url_for, session, g
from dotenv import load_dotenv
from sqlalchemy.orm import joinedload

# --- Importaciones de la Aplicación ---
from models.base import db, User, Role

# Cargar variables de entorno
load_dotenv()

def create_app(config_name='default'):
    """Application Factory: Crea y configura la aplicación Flask."""
    app = Flask(__name__)

    # --- Configuración ---
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'una-clave-secreta-de-desarrollo-super-segura')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///sistemacom.db')
    app.jinja_env.add_extension('jinja2.ext.do') # Necesario para algunas plantillas

    # --- Inicializar extensiones ---
    db.init_app(app)

    # --- Registrar Blueprints ---
    from blueprints.auth.routes import auth_bp
    from blueprints.dashboard.routes import dashboard_bp
    from blueprints.superadmin.routes import superadmin_bp
    from blueprints.products.routes import products_bp
    from blueprints.purchases.routes import purchases_bp
    from blueprints.invoices.routes import invoices_bp
    from blueprints.crm.routes import crm_bp
    from blueprints.reports.routes import reports_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(superadmin_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(purchases_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(crm_bp)
    app.register_blueprint(reports_bp)

    # --- Middleware y Rutas Principales ---
    @app.before_request
    def before_request():
        """Carga el usuario y su tenant en el contexto global `g`."""
        g.user = None
        g.tenant = None
        if 'user_id' in session:
            # Carga optimizada de usuario, roles y permisos
            user = db.session.query(User).options(
                joinedload(User.roles).joinedload(Role.permissions)
            ).get(session.get('user_id'))

            if user:
                g.user = user
                g.tenant = user.client if user.role != 'superadmin' else None

    @app.route('/')
    def index():
        """Redirige al dashboard apropiado si hay sesión, si no, al login."""
        if g.user:
            if g.user.role == 'superadmin':
                return redirect(url_for('superadmin.superadmin'))
            return redirect(url_for('dashboard.dashboard'))
        return redirect(url_for('auth.login'))

    # --- Comandos CLI ---
    @app.cli.command("init-db")
    def init_db_command():
        """Inicializa la base de datos con datos de prueba."""
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
    app.run(debug=True, port=8000, host='0.0.0.0')