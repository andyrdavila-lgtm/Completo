import os
from app import create_app, db
from utils.initialization import initialize_system_data, create_demo_users

# Crear una instancia de la app para obtener el contexto de la aplicación
app = create_app()

with app.app_context():
    print("--- Iniciando configuración de la base de datos ---")

    # Eliminar la base de datos anterior si existe para un inicio limpio
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🗑️ Base de datos '{db_path}' anterior eliminada.")

    print("🗃️ Creando todas las tablas...")
    db.create_all()
    print("✅ Tablas creadas.")

    print("\n🌱 Poblando la base de datos con datos iniciales...")
    initialize_system_data()
    create_demo_users()

    print("\n🎉 Base de datos local creada y poblada exitosamente.")
    print("🔑 Credenciales del Superadmin: superadmin / admin123")
    print("🔑 Credenciales de Demo: admin_demo / demo123")
    print("--- Configuración de la base de datos finalizada ---")