from models.base import db, BusinessType, Client, User
from werkzeug.security import generate_password_hash

def initialize_system_data():
    """Inicializar datos básicos del sistema"""
    try:
        # Verificar si ya existen tipos de negocio
        if BusinessType.query.count() == 0:
            print("🏢 Creando tipos de negocio...")
            
            business_types = [
                BusinessType(name='Restaurante', description='Restaurantes y servicios de comida'),
                BusinessType(name='Retail', description='Tiendas y comercio minorista'),
                BusinessType(name='Servicios', description='Servicios profesionales'),
                BusinessType(name='Hoteleria', description='Hoteles y hospedaje'),
                BusinessType(name='Salud', description='Clínicas y servicios de salud'),
            ]
            
            for business_type in business_types:
                db.session.add(business_type)
            
            db.session.commit()
            print("✅ Tipos de negocio creados")
        
        print("✅ Datos del sistema inicializados")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error inicializando datos del sistema: {e}")
        raise

def create_demo_users():
    """Crear usuarios de demostración"""
    try:
        # Verificar si el superadmin ya existe
        if not User.query.filter_by(username='superadmin').first():
            print("👑 Creando superadmin...")
            
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
            print("✅ Superadmin creado")
        
        print("✅ Usuarios demo creados")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creando usuarios demo: {e}")
        raise