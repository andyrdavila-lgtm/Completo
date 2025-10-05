"""
Pruebas para el módulo de gestión de productos.
"""
from models.base import db, Product, User

def test_products_page_unauthorized(client):
    """
    Test: Un usuario no autenticado no puede acceder a la página de productos.
    """
    response = client.get('/products/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Debes iniciar sesi\xc3\xb3n para ver esta p\xc3\xa1gina.' in response.data

def test_products_page_authorized(client):
    """
    Test: Un usuario autorizado (admin_demo) puede acceder a la página de productos.
    """
    with client:
        client.post('/auth/login', data={'username': 'admin_demo', 'password': 'demo123'})
        response = client.get('/products/')
        assert response.status_code == 200
        assert b'<h2>Gestionar Productos</h2>' in response.data

def test_product_crud(client):
    """
    Test: Probar el ciclo completo de CRUD para un producto.
    La prueba se centra en la persistencia en la base de datos.
    """
    with client:
        # Iniciar sesión
        client.post('/auth/login', data={'username': 'admin_demo', 'password': 'demo123'})

        demo_user = User.query.filter_by(username='admin_demo').first()
        assert demo_user and demo_user.client_id is not None

        # 1. CREATE
        create_response = client.post('/products/create', data={
            'name': 'Laptop Pro',
            'sku': 'LP-123',
            'price': '1500.50',
            'stock': '50'
        }, follow_redirects=True)
        assert create_response.status_code == 200

        # 2. READ (Verificar en la BD)
        product = Product.query.filter_by(sku='LP-123').first()
        assert product is not None
        assert product.name == 'Laptop Pro'

        # 3. UPDATE
        client.post(f'/products/{product.id}/edit', data={
            'name': 'Laptop Pro X',
            'price': '1550.00',
            'stock': '45'
        }, follow_redirects=True)

        updated_product = db.session.get(Product, product.id)
        assert updated_product.name == 'Laptop Pro X'

        # 4. DELETE
        client.post(f'/products/{product.id}/delete', follow_redirects=True)

        assert db.session.get(Product, product.id) is None