import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models.base import User, Client

def check_database():
    with app.app_context():
        print("=== VERIFICACIÓN DE BASE DE DATOS ===")
        
        # Verificar usuarios
        users = User.query.all()
        print(f"\nTotal de usuarios: {len(users)}")
        
        for user in users:
            print(f"\nUsuario: {user.username}")
            print(f"  ID: {user.id}")
            print(f"  Client ID: {user.client_id}")
            print(f"  Rol: {user.role}")
            print(f"  Activo: {user.is_active}")
            print(f"  Bloqueado: {user.is_blocked}")
            
            # Verificar si el cliente existe
            client = Client.query.get(user.client_id)
            if client:
                print(f"  Cliente: {client.business_name}")
            else:
                print(f"  ⚠️ CLIENTE NO ENCONTRADO para client_id: {user.client_id}")
        
        # Verificar clientes
        clients = Client.query.all()
        print(f"\nTotal de clientes: {len(clients)}")
        
        for client in clients:
            print(f"\nCliente: {client.business_name}")
            print(f"  ID: {client.id}")
            print(f"  Activo: {client.is_active}")
            
            # Verificar usuarios del cliente
            client_users = User.query.filter_by(client_id=client.id).all()
            print(f"  Usuarios: {len(client_users)}")
        
        print("\n=== VERIFICACIÓN COMPLETADA ===")

if __name__ == '__main__':
    check_database()