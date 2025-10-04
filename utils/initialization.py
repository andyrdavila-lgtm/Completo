from models.base import db, BusinessType, Client, User, Permission, Role
from werkzeug.security import generate_password_hash

def create_initial_permissions():
    """Crea los permisos iniciales del sistema si no existen."""
    print("🔎 Verificando permisos del sistema...")

    permissions_to_create = {
        'superadmin.dashboard.view': 'Ver el dashboard del superadministrador',
        'superadmin.roles.manage': 'Gestionar roles y permisos',
        'superadmin.clients.view': 'Ver la lista de clientes',
        'superadmin.clients.create': 'Crear nuevos clientes',
        'superadmin.clients.edit': 'Editar clientes existentes',
        'superadmin.clients.delete': 'Eliminar clientes',
        'dashboard.view': 'Ver el dashboard del cliente',
        'users.view': 'Ver la lista de usuarios del cliente',
        'users.create': 'Crear nuevos usuarios para el cliente',
        'users.edit': 'Editar usuarios del cliente',
        'users.delete': 'Eliminar usuarios del cliente',
        'reports.view': 'Ver los informes del cliente',
    }

    existing_permissions = {p.name for p in Permission.query.all()}

    new_permissions = []
    for name, description in permissions_to_create.items():
        if name not in existing_permissions:
            new_permissions.append(Permission(name=name, description=description))

    if new_permissions:
        print(f"✨ Creando {len(new_permissions)} nuevos permisos...")
        db.session.add_all(new_permissions)
        db.session.commit()
        print("✅ Permisos creados.")
    else:
        print("✅ Permisos ya están al día.")

def initialize_system_data():
    """Inicializar datos básicos del sistema (Tipos de negocio, Permisos y Roles)."""
    try:
        # Crear tipos de negocio
        if BusinessType.query.count() == 0:
            print("🏢 Creando tipos de negocio...")
            business_types = [
                BusinessType(name='Restaurante', description='Restaurantes y servicios de comida'),
                BusinessType(name='Retail', description='Tiendas y comercio minorista'),
                BusinessType(name='Servicios', description='Servicios profesionales'),
                BusinessType(name='Hoteleria', description='Hoteles y hospedaje'),
                BusinessType(name='Salud', description='Clínicas y servicios de salud'),
            ]
            db.session.add_all(business_types)
            db.session.commit()
            print("✅ Tipos de negocio creados.")

        # Crear permisos y roles por defecto
        create_initial_permissions()
        create_default_roles()

        print("✅ Datos del sistema inicializados correctamente.")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error inicializando datos del sistema: {e}")
        raise

def create_default_roles():
    """Crea los roles por defecto si no existen."""
    print("🔎 Verificando roles del sistema...")
    if Role.query.filter_by(name='Administrador de Cliente').first():
        print("✅ Roles por defecto ya existen.")
        return

    print("✨ Creando rol 'Administrador de Cliente'...")
    admin_role = Role(name='Administrador de Cliente', description='Rol con permisos para administrar un cliente específico.')

    # Asignar permisos básicos al rol de administrador
    permissions_for_admin = [
        'dashboard.view',
        'users.view',
        'users.create',
        'users.edit',
        'reports.view'
    ]
    permissions = Permission.query.filter(Permission.name.in_(permissions_for_admin)).all()
    admin_role.permissions.extend(permissions)

    db.session.add(admin_role)
    db.session.commit()
    print("✅ Rol 'Administrador de Cliente' creado con permisos básicos.")

def create_demo_users():
    """Crear usuarios de demostración (superadmin y un cliente de ejemplo)."""
    try:
        # --- Superadmin ---
        if not User.query.filter_by(username='superadmin').first():
            print("👑 Creando usuario superadmin...")
            superadmin = User(
                username='superadmin',
                email='superadmin@sistemacom.com',
                first_name='Super',
                last_name='Admin',
                role='superadmin'
            )
            superadmin.set_password('admin123')
            db.session.add(superadmin)
            print("✅ Superadmin creado (usuario: superadmin, contraseña: admin123).")

        # --- Cliente y Usuario de Demostración ---
        if not Client.query.filter_by(name='Cliente Demo').first():
            print("🏢 Creando cliente y usuario de demostración...")
            demo_client = Client(name='Cliente Demo', email='demo@cliente.com', business_type_id=1)
            db.session.add(demo_client)

            admin_role = Role.query.filter_by(name='Administrador de Cliente').first()

            demo_user = User(
                username='admin_demo',
                email='admin@cliente.demo',
                first_name='Admin',
                last_name='Demo',
                client=demo_client
            )
            demo_user.set_password('demo123')
            if admin_role:
                demo_user.roles.append(admin_role)

            db.session.add(demo_user)
            print("✅ Cliente Demo y usuario admin_demo creados (contraseña: demo123).")

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creando usuarios demo: {e}")
        raise