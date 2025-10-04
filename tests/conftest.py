import pytest
import os

# Añadir el directorio raíz al path para que encuentre la app
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from utils.initialization import initialize_system_data, create_demo_users

@pytest.fixture(scope='module')
def app():
    """
    Fixture que crea y configura una nueva instancia de la app para cada módulo de prueba.
    """
    # El config_name 'testing' asegura que se use la config de testing (SQLite en memoria)
    app = create_app(config_name='testing')

    # Establecer un contexto de aplicación
    with app.app_context():
        # Crear las tablas de la base de datos
        db.create_all()

        # Poblar con datos iniciales necesarios para las pruebas
        initialize_system_data()
        create_demo_users()

        yield app

        # Limpieza: eliminar la base de datos
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    """Un cliente de pruebas para la app."""
    return app.test_client()

@pytest.fixture(scope='module')
def runner(app):
    """Un runner para comandos CLI de la app."""
    return app.test_cli_runner()