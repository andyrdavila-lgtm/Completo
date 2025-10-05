import pytest
import os

# Añadir el directorio raíz al path para que encuentre la app
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from utils.initialization import initialize_system_data, create_demo_users

@pytest.fixture(scope='module')
def app():
    """Crea y configura una nueva instancia de la app para cada módulo de prueba."""
    app = create_app(config_name='testing')

    with app.app_context():
        db.create_all()
        initialize_system_data()
        create_demo_users()
        yield app
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    """Un cliente de pruebas para la app."""
    return app.test_client()