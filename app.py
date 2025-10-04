import sys
import os

# Agregar el directorio actual al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, session, g, redirect, url_for
from flask_migrate import Migrate
import urllib.parse
from datetime import timedelta
from models.base import db

# --- CONFIGURACIÓN DE BASE DE DATOS SQL SERVER ---
DB_SERVER = 'localhost'
DB_NAME = 'SISTEMACOM'
DB_DRIVER = 'ODBC Driver 17 for SQL Server'

DB_CONNECTION_STRING = (
    f'DRIVER={{{DB_DRIVER}}};'
    f'SERVER={DB_SERVER};'
    f'DATABASE={DB_NAME};'
    f'Trusted_Connection=yes;'
)

encoded_connection_string = urllib.parse.quote_plus(DB_CONNECTION_STRING)
SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={encoded_connection_string}"

app = Flask(__name__)

# Configuración
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = 'mi-clave-secreta-muy-segura-sistemacom-2025'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
app.config['DEBUG'] = True

# Inicializar extensiones
db.init_app(app)
migrate = Migrate(app, db)

# Importar blueprints
try:
    from blueprints.auth.routes import auth_bp
    from blueprints.dashboard.routes import dashboard_bp
    from blueprints.users.routes import users_bp
    from blueprints.clients.routes import clients_bp
    from blueprints.reports.routes import reports_bp
    from blueprints.superadmin.routes import superadmin_bp
    
    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(clients_bp, url_prefix='/clients')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    app.register_blueprint(superadmin_bp, url_prefix='/superadmin')
    
    print("✅ Blueprints cargados correctamente")
    
except ImportError as e:
    print(f"❌ Error cargando blueprints: {e}")
    import traceback
    traceback.print_exc()

# Middleware
@app.before_request
def before_request():
    """Configuración antes de cada request"""
    from models.base import User, Client
    from blueprints.core.auth import get_user_modules  # Corregido
    
    g.user = None
    g.tenant = None
    g.modules = []
    
    if 'user_id' in session:
        g.user = db.session.get(User, session['user_id'])
        
        if g.user:
            print(f"👤 Usuario en sesión: {g.user.username}, rol: {g.user.role}")
            
            if g.user.role == 'superadmin':
                print("🔧 Usuario es superadmin - omitiendo verificación de tenant")
                g.tenant = None
                g.modules = []
            else:
                if 'client_id' in session:
                    g.tenant = db.session.get(Client, session['client_id'])
                    if g.tenant:
                        g.modules = get_user_modules(session['user_id'], session['client_id'])
                    else:
                        print(f"❌ Cliente no encontrado para client_id: {session['client_id']}")
                        session.clear()
                        return redirect(url_for('auth.login'))

@app.route('/')
def index():
    """Ruta principal"""
    if 'user_id' in session:
        user = g.user
        if user and user.role == 'superadmin':
            return redirect(url_for('superadmin.superadmin'))
        else:
            return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.login'))

# Inicialización del sistema
def initialize_system():
    """Inicializar sistema"""
    with app.app_context():
        try:
            # Crear tablas
            print("🗃️ Creando tablas en la base de datos...")
            db.create_all()
            print("✅ Tablas de base de datos creadas")
            
            # Inicializar datos básicos
            from utils.initialization import initialize_system_data, create_demo_users
            initialize_system_data()
            create_demo_users()
            
            print("🎉 Sistema inicializado correctamente")
            
        except Exception as e:
            print(f"❌ Error durante la inicialización: {e}")

if __name__ == '__main__':
    initialize_system()
    
    print("\n" + "="*60)
    print("🚀 SISTEMA SISTEMACOM INICIADO CORRECTAMENTE")
    print("="*60)
    print("📍 Servidor ejecutándose en: http://localhost:8000")
    print("👤 Credenciales de acceso:")
    print("   • Super Administrador: superadmin / admin123")
    print("   • Usuarios demo: ver logs de inicialización")
    print("="*60)
    
    app.run(debug=app.config['DEBUG'], port=8000, host='0.0.0.0')