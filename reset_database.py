import sys
import os
import urllib.parse
from flask import Flask

# Configuración de base de datos
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

# Crear app Flask temporal
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Importar después de crear la app para evitar dependencias circulares
from models.base import db, BusinessType, Client, User
db.init_app(app)

def reset_database():
    with app.app_context():
        try:
            print("🗑️ Eliminando tablas existentes...")
            db.drop_all()
            
            print("🗃️ Creando nuevas tablas...")
            db.create_all()
            
            print("📝 Creando datos iniciales...")
            
            # Crear tipos de negocio
            business_types = [
                BusinessType(name='Restaurante', description='Restaurantes y servicios de comida'),
                BusinessType(name='Cafetería', description='Cafeterías y coffee shops'),
                BusinessType(name='Bar', description='Bares y cantinas'),
                BusinessType(name='Hotel', description='Hoteles y hospedaje'),
                BusinessType(name='Retail', description='Tiendas minoristas'),
            ]
            
            for bt in business_types:
                db.session.add(bt)
            
            db.session.commit()
            
            # Crear superadmin
            superadmin = User(
                username='superadmin',
                email='superadmin@sistemacom.com',
                first_name='Super',
                last_name='Administrador',
                role='superadmin'
            )
            superadmin.set_password('admin123')
            db.session.add(superadmin)
            
            db.session.commit()
            
            print("✅ Base de datos resetada correctamente")
            print("👤 Superadmin creado: superadmin / admin123")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    reset_database()