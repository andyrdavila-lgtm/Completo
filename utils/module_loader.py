import os
import importlib.util
from flask import current_app

def load_module_routes(app):
    """Carga dinámicamente las rutas de los módulos"""
    modules_dir = app.config.get('MODULES_DIR', 'modules')
    
    # Asegurar ruta absoluta (si el valor es relativo, se interpreta respecto a app.root_path)
    if not os.path.isabs(modules_dir):
        modules_dir = os.path.join(app.root_path, modules_dir)
    
    if not os.path.exists(modules_dir):
        print(f"Directorio de módulos '{modules_dir}' no encontrado")
        return
    
    for module_name in os.listdir(modules_dir):
        module_path = os.path.join(modules_dir, module_name, 'routes.py')
        
        if os.path.isfile(module_path):
            try:
                # Cargar el módulo dinámicamente
                spec = importlib.util.spec_from_file_location(f"{module_name}.routes", module_path)
                if spec is None or spec.loader is None:
                    print(f"No se pudo crear spec para {module_name}")
                    continue
                module = importlib.util.module_from_spec(spec)
                # Ejecutar la carga dentro del contexto de la app por si el módulo usa current_app
                with app.app_context():
                    spec.loader.exec_module(module)
                    # Registrar las rutas con la aplicación
                    if hasattr(module, 'register_routes'):
                        module.register_routes(app)
                        print(f"Módulo '{module_name}' cargado correctamente")
                    
            except Exception as e:
                print(f"Error cargando módulo {module_name}: {str(e)}")