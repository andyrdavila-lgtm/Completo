import os
from datetime import timedelta

# Configuración básica
SECRET_KEY = os.environ.get('SECRET_KEY') or 'mi-clave-secreta-muy-segura'
DEBUG = True

# Configuración de base de datos
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuración de sesión
PERMANENT_SESSION_LIFETIME = timedelta(days=1)

# Configuración de módulos
MODULES_DIR = 'modules'

# Configuración de servidor
SERVER_HOST = 'localhost'
SERVER_PORT = 8000
