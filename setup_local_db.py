import os
from app import create_app, db
from utils.initialization import initialize_system_data, create_demo_users

# --- Configuración ---
# Nombre del archivo de la base de datos SQLite
DB_FILENAME = "sistemacom.db"

# Eliminar la base de datos anterior si existe, para empezar de cero
if os.path.exists(DB_FILENAME):
    os.remove(DB_FILENAME)
    print(f"🗑️ Base de datos '{DB_FILENAME}' anterior eliminada.")

# Crear una instancia de la app configurada para usar SQLite
# Forzamos la configuración 'testing' para que use SQLite, pero apuntando a un archivo físico
os.environ['TEST_DATABASE_URL'] = f'sqlite:///{DB_FILENAME}'
app = create_app(config_name='testing')

# --- Proceso de Inicialización ---
with app.app_context():
    print(f"🗃️ Creando base de datos en '{DB_FILENAME}'...")
    db.create_all()
    print("✅ Tablas creadas.")

    print("\n🌱 Poblando la base de datos con datos iniciales...")
    initialize_system_data()
    create_demo_users()

    print("\n🎉 Base de datos local creada y poblada exitosamente.")
    print(f"🔑 Credenciales del Superadmin: superadmin / admin123")