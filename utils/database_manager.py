from models.base import db, BusinessType, Client, User, Module, ClientModule, UserModule
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def initialize_system():
    """Inicializa los datos del sistema con la nueva estructura"""
    
    # Crear tipos de negocio
    business_types = [
        {'name': 'Restaurante', 'description': 'Negocio de comida y bebidas'},
        {'name': 'Retail', 'description': 'Tienda de venta al por menor'},
        {'name': 'Servicios', 'description': 'Empresa de servicios profesionales'},
        {'name': 'Manufactura', 'description': 'Empresa de fabricación'},
        {'name': 'Salud', 'description': 'Clínicas y centros de salud'},
        {'name': 'Educación', 'description': 'Instituciones educativas'},
        {'name': 'Tecnología', 'description': 'Empresas de tecnología'},
        {'name': 'Otros', 'description': 'Otros tipos de negocio'}
    ]
    
    for bt_data in business_types:
        business_type = BusinessType.query.filter_by(name=bt_data['name']).first()
        if not business_type:
            business_type = BusinessType(
                name=bt_data['name'],
                description=bt_data['description']
            )
            db.session.add(business_type)
    
    db.session.commit()
    print("Tipos de negocio creados")
    
    # Crear módulos del sistema
    system_modules = [
        # Módulos core (esenciales)
        {'name': 'dashboard', 'display_name': 'Dashboard', 'route': '/dashboard', 
         'icon': 'fas fa-tachometer-alt', 'category': 'core', 'is_core': True, 'price_tier': 'basic'},
        {'name': 'profile', 'display_name': 'Perfil', 'route': '/profile', 
         'icon': 'fas fa-user', 'category': 'core', 'is_core': True, 'price_tier': 'basic'},
        
        # Módulos básicos
        {'name': 'facturacion', 'display_name': 'Facturación', 'route': '/facturacion', 
         'icon': 'fas fa-file-invoice', 'category': 'ventas', 'price_tier': 'basic'},
        {'name': 'compras', 'display_name': 'Compras', 'route': '/compras', 
         'icon': 'fas fa-shopping-cart', 'category': 'compras', 'price_tier': 'basic'},
        {'name': 'inventario', 'display_name': 'Inventario', 'route': '/inventario', 
         'icon': 'fas fa-boxes', 'category': 'operaciones', 'price_tier': 'basic'},
        
        # Módulos premium
        {'name': 'reportes', 'display_name': 'Reportes Avanzados', 'route': '/reportes', 
         'icon': 'fas fa-chart-bar', 'category': 'analytics', 'price_tier': 'premium'},
        {'name': 'crm', 'display_name': 'CRM', 'route': '/crm', 
         'icon': 'fas fa-users', 'category': 'ventas', 'price_tier': 'premium'},
        
        # Módulos enterprise
        {'name': 'menu_digital', 'display_name': 'Menú Digital', 'route': '/menu-digital', 
         'icon': 'fas fa-utensils', 'category': 'restaurantes', 'price_tier': 'enterprise'},
        {'name': 'reservas', 'display_name': 'Sistema de Reservas', 'route': '/reservas', 
         'icon': 'fas fa-calendar-check', 'category': 'restaurantes', 'price_tier': 'enterprise'},
        {'name': 'backups', 'display_name': 'Backups Automáticos', 'route': '/backups', 
         'icon': 'fas fa-database', 'category': 'sistema', 'price_tier': 'enterprise'},
        {'name': 'api', 'display_name': 'API Integration', 'route': '/api-config', 
         'icon': 'fas fa-code', 'category': 'sistema', 'price_tier': 'enterprise'},
    ]
    
    for module_data in system_modules:
        module = Module.query.filter_by(name=module_data['name']).first()
        if not module:
            module = Module(**module_data)
            db.session.add(module)
    
    db.session.commit()
    print("Módulos del sistema creados")
    
    # Crear cliente de ejemplo (Andre - Restaurante)
    restaurante_type = BusinessType.query.filter_by(name='Restaurante').first()
    
    example_client = Client.query.filter_by(owner_email='andre@restaurante.com').first()
    if not example_client:
        example_client = Client(
            owner_names='Andre García',
            owner_email='andre@restaurante.com',
            owner_phone='+1234567890',
            business_name='Restaurante La Buena Mesa',
            business_type_id=restaurante_type.id,
            max_users=5,
            subscription_plan='premium',
            subscription_status='active',
            subscription_start=datetime.utcnow(),
            subscription_end=datetime.utcnow() + timedelta(days=365)
        )
        db.session.add(example_client)
        db.session.commit()
        print("Cliente ejemplo (Andre) creado")
        
        # Asignar módulos al cliente
        basic_modules = Module.query.filter(
            (Module.price_tier == 'basic') | 
            (Module.is_core == True)
        ).all()
        
        premium_modules = Module.query.filter_by(price_tier='premium').all()
        
        # Asignar todos los módulos básicos y premium (por ser plan premium)
        for module in basic_modules + premium_modules:
            client_module = ClientModule(
                client_id=example_client.id,
                module_id=module.id,
                is_active=True
            )
            db.session.add(client_module)
        
        db.session.commit()
        print("Módulos asignados al cliente ejemplo")
        
        # Crear usuario owner (Andre)
        owner_user = User(
            username='andre',
            email='andre@restaurante.com',
            password_hash=generate_password_hash('andre123'),
            full_name='Andre García',
            phone='+1234567890',
            role='owner',
            client_id=example_client.id
        )
        db.session.add(owner_user)
        
        # Crear empleados de ejemplo
        employees_data = [
            {'username': 'maria', 'email': 'maria@restaurante.com', 'password': 'maria123', 
             'full_name': 'Maria López', 'role': 'manager'},
            {'username': 'carlos', 'email': 'carlos@restaurante.com', 'password': 'carlos123', 
             'full_name': 'Carlos Ruiz', 'role': 'employee'},
            {'username': 'lucia', 'email': 'lucia@restaurante.com', 'password': 'lucia123', 
             'full_name': 'Lucía Mendoza', 'role': 'employee'},
        ]
        
        for emp_data in employees_data:
            employee = User(
                username=emp_data['username'],
                email=emp_data['email'],
                password_hash=generate_password_hash(emp_data['password']),
                full_name=emp_data['full_name'],
                role=emp_data['role'],
                client_id=example_client.id
            )
            db.session.add(employee)
        
        db.session.commit()
        print("Usuarios empleados creados para el cliente ejemplo")
        
        # Asignar permisos de módulos a los usuarios
        client_modules = ClientModule.query.filter_by(client_id=example_client.id).all()
        
        for user in [owner_user] + [User.query.filter_by(username=emp['username']).first() for emp in employees_data]:
            for client_module in client_modules:
                user_module = UserModule(
                    user_id=user.id,
                    module_id=client_module.module_id,
                    can_view=True,
                    can_edit=user.role in ['owner', 'manager'],
                    can_delete=user.role == 'owner',
                    can_manage=user.role == 'owner'
                )
                db.session.add(user_module)
        
        db.session.commit()
        print("Permisos de módulos asignados a usuarios")
    
    # Crear superadmin del sistema
    superadmin_client = Client.query.filter_by(business_name='Sistema A&D').first()
    if not superadmin_client:
        otros_type = BusinessType.query.filter_by(name='Otros').first()
        
        superadmin_client = Client(
            owner_names='Administrador del Sistema',
            owner_email='admin@ayd.com',
            owner_phone='+0000000000',
            business_name='Sistema A&D',
            business_type_id=otros_type.id,
            max_users=1,
            subscription_plan='enterprise',
            subscription_status='active'
        )
        db.session.add(superadmin_client)
        db.session.commit()
    
    superadmin_user = User.query.filter_by(username='admin').first()
    if not superadmin_user:
        superadmin_user = User(
            username='admin',
            email='admin@ayd.com',
            password_hash=generate_password_hash('admin123'),
            full_name='Super Administrador',
            role='superadmin',
            client_id=superadmin_client.id
        )
        db.session.add(superadmin_user)
        
        # El superadmin tiene acceso a todos los módulos
        all_modules = Module.query.all()
        for module in all_modules:
            user_module = UserModule(
                user_id=superadmin_user.id,
                module_id=module.id,
                can_view=True,
                can_edit=True,
                can_delete=True,
                can_manage=True
            )
            db.session.add(user_module)
        
        db.session.commit()
        print("Superadmin creado con acceso completo")
    
    print("Sistema inicializado correctamente con la nueva estructura")