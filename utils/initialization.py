from models.base import db, BusinessType, Client, User, Permission, Role
from werkzeug.security import generate_password_hash

def create_initial_permissions():
    """Crea todos los permisos necesarios para el sistema."""
    permissions_to_create = {
        'superadmin.dashboard.view': 'Ver el dashboard del superadministrador',
        'superadmin.roles.manage': 'Gestionar roles y permisos',
        'superadmin.clients.manage': 'Gestionar clientes (CRUD)',
        'dashboard.view': 'Ver el dashboard del cliente',
        'users.manage': 'Gestionar usuarios del cliente',
        'products.manage': 'Gestionar productos del cliente',
        'purchases.manage': 'Gestionar órdenes de compra',
        'invoices.manage': 'Gestionar facturas',
        'crm.manage': 'Gestionar CRM',
        'reports.view': 'Ver informes del cliente',
    }

    existing_permissions = {p.name for p in Permission.query.all()}

    for name, description in permissions_to_create.items():
        if name not in existing_permissions:
            db.session.add(Permission(name=name, description=description))

    db.session.commit()

def create_default_roles():
    """Crea o actualiza los roles por defecto del sistema."""
    role_name = 'Administrador de Cliente'
    expected_permissions = {
        'dashboard.view', 'users.manage', 'products.manage',
        'purchases.manage', 'invoices.manage', 'crm.manage', 'reports.view'
    }

    admin_role = Role.query.filter_by(name=role_name).first()
    if not admin_role:
        admin_role = Role(name=role_name, description='Rol con permisos para administrar un cliente.')
        db.session.add(admin_role)

    current_permissions = {p.name for p in admin_role.permissions}
    missing_permissions = expected_permissions - current_permissions

    if missing_permissions:
        permissions_to_add = Permission.query.filter(Permission.name.in_(missing_permissions)).all()
        admin_role.permissions.extend(permissions_to_add)

    db.session.commit()

def initialize_system_data():
    """Inicializa los datos básicos del sistema."""
    create_initial_permissions()
    create_default_roles()

def create_demo_users():
    """Crea el superadmin y un cliente de demostración con su usuario."""
    if not User.query.filter_by(username='superadmin').first():
        superadmin = User(username='superadmin', email='superadmin@sistemacom.com', role='superadmin')
        superadmin.set_password('admin123')
        db.session.add(superadmin)

    if not Client.query.filter_by(name='Cliente Demo').first():
        demo_client = Client(name='Cliente Demo')
        db.session.add(demo_client)
        db.session.flush()

        admin_role = Role.query.filter_by(name='Administrador de Cliente').first()
        demo_user = User(
            username='admin_demo',
            email='admin@cliente.demo',
            client_id=demo_client.id
        )
        demo_user.set_password('demo123')
        if admin_role:
            demo_user.roles.append(admin_role)
        db.session.add(demo_user)

    db.session.commit()