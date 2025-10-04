"""
Pruebas básicas para la aplicación Flask.
Verifica el acceso a páginas, login y rutas protegidas.
"""
from flask import request

def test_index_redirects_to_login(client):
    """
    Test: La ruta raíz '/' debe redirigir a '/auth/login' si no hay sesión.
    """
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
    # Comprobar que el contenido de la página de login está presente
    assert b'<h1 class="card-title text-center">Login</h1>' in response.data


def test_login_page_loads(client):
    """
    Test: La página de login '/auth/login' debe cargarse correctamente.
    """
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'<h1 class="card-title text-center">Login</h1>' in response.data


def test_superadmin_login_logout(client):
    """
    Test: El superadministrador debe poder iniciar y cerrar sesión.
    """
    # Probar login con credenciales correctas
    response = client.post('/auth/login', data={
        'username': 'superadmin',
        'password': 'admin123'
    }, follow_redirects=True)

    assert response.status_code == 200
    # Comprobar que se ha redirigido al dashboard del superadmin
    assert b'<h2>Dashboard del Superadministrador</h2>' in response.data

    # Probar que una ruta protegida es accesible
    response = client.get('/superadmin/roles')
    assert response.status_code == 200
    assert b'<h2>Gestionar Roles y Permisos</h2>' in response.data

    # Probar logout
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    # Comprobar que se ha redirigido a la página de login
    assert b'<h1 class="card-title text-center">Login</h1>' in response.data
    assert b'Has cerrado sesi\xc3\xb3n' in response.data # 'Has cerrado sesión' en bytes


def test_invalid_login(client):
    """
    Test: Un intento de login con credenciales incorrectas debe fallar.
    """
    response = client.post('/auth/login', data={
        'username': 'superadmin',
        'password': 'wrongpassword'
    }, follow_redirects=True)

    assert response.status_code == 200
    # Comprobar que permanece en la página de login y muestra un error
    assert b'<h1 class="card-title text-center">Login</h1>' in response.data
    assert b'Usuario o contrase\xc3\xb1a incorrectos' in response.data # 'Usuario o contraseña incorrectos'


def test_protected_route_access_denied(client):
    """
    Test: Un usuario no autenticado no puede acceder a una ruta protegida.
    """
    response = client.get('/superadmin/clients', follow_redirects=True)
    assert response.status_code == 200
    # Comprobar que es redirigido al login y se muestra un mensaje de advertencia
    assert b'<h1 class="card-title text-center">Login</h1>' in response.data
    assert b'Debes iniciar sesi\xc3\xb3n para ver esta p\xc3\xa1gina.' in response.data # 'Debes iniciar sesión...'