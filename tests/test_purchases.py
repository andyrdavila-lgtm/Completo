"""
Pruebas para el módulo de gestión de compras.
"""
from models.base import db, PurchaseOrder, Product, User
import json

def test_purchases_page_unauthorized(client):
    """
    Test: Un usuario no autenticado no puede acceder a la página de compras.
    """
    response = client.get('/purchases/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Debes iniciar sesi\xc3\xb3n para ver esta p\xc3\xa1gina.' in response.data

def test_purchases_page_authorized(client):
    """
    Test: Un usuario autorizado (admin_demo) puede acceder a la página de compras.
    """
    with client:
        client.post('/auth/login', data={'username': 'admin_demo', 'password': 'demo123'})
        response = client.get('/purchases/')
        assert response.status_code == 200
        assert b'<h2>\xc3\x93rdenes de Compra</h2>' in response.data # "Órdenes de Compra"

def test_create_purchase_order(client):
    """
    Test: Probar la creación de una nueva orden de compra.
    """
    with client:
        client.post('/auth/login', data={'username': 'admin_demo', 'password': 'demo123'})

        demo_user = User.query.filter_by(username='admin_demo').first()
        assert demo_user and demo_user.client_id is not None

        # Crear un producto de prueba
        test_product = Product(name="Producto de Prueba Compra", price=10.0, stock=100, client_id=demo_user.client_id)
        db.session.add(test_product)
        db.session.commit()

        # Datos para la nueva orden
        items_data = [{"product_id": test_product.id, "quantity": 5, "price": 8.50}]

        response_create = client.post('/purchases/create', data={
            'supplier': 'Proveedor XYZ',
            'order_date': '2025-10-26',
            'items_data': json.dumps(items_data)
        }, follow_redirects=True)

        assert response_create.status_code == 200
        assert b'Orden de compra creada exitosamente.' in response_create.data

        # Verificar en la BD
        order = PurchaseOrder.query.filter_by(supplier='Proveedor XYZ').first()
        assert order is not None
        assert len(order.items) == 1
        assert order.items[0].quantity == 5
        assert order.total_amount == 42.50