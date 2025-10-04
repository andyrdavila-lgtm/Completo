class TenantManager:
    def __init__(self, app):
        self.app = app
    
    def get_tenant_by_subdomain(self, subdomain):
        from models.base import Tenant
        return Tenant.query.filter_by(subdomain=subdomain).first()
    
    def initialize_tenant(self, tenant_id):
        """Inicializa los módulos por defecto para un tenant"""
        from models.base import Module, db
        
        default_modules = [
            {
                'name': 'dashboard',
                'display_name': 'Dashboard',
                'route': '/dashboard',
                'icon': 'fas fa-tachometer-alt'
            },
            {
                'name': 'facturacion',
                'display_name': 'Facturación',
                'route': '/facturacion',
                'icon': 'fas fa-file-invoice'
            },
            {
                'name': 'compras',
                'display_name': 'Compras',
                'route': '/compras',
                'icon': 'fas fa-shopping-cart'
            },
            {
                'name': 'reportes',
                'display_name': 'Reportes',
                'route': '/reportes',
                'icon': 'fas fa-chart-bar'
            },
            {
                'name': 'backups',
                'display_name': 'Backups',
                'route': '/backups',
                'icon': 'fas fa-database'
            },
            {
                'name': 'configuracion',
                'display_name': 'Configuración',
                'route': '/configuracion',
                'icon': 'fas fa-cog'
            },
            {
                'name': 'menu_digital',
                'display_name': 'Menú Digital',
                'route': '/menu-digital',
                'icon': 'fas fa-utensils'
            }
        ]
        
        for module_data in default_modules:
            module = Module(
                name=module_data['name'],
                display_name=module_data['display_name'],
                route=module_data['route'],
                icon=module_data['icon'],
                tenant_id=tenant_id
            )
            db.session.add(module)
        
        db.session.commit()