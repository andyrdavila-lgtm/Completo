import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models.base import User, Client

def fix_database():
    with app.app_context():
        print("=== REPARANDO BASE DE DATOS ===")
        
        # Encontrar el cliente del sistema (Sistema A&D)
        system_client = Client.query.filter_by(business_name='Sistema A&D').first()
        if not system_client:
            print("❌ No se encontró el cliente del sistema")
            return
        
        print(f"Cliente del sistema encontrado: {system_client.business_name} (ID: {system_client.id})")
        
        # Reparar usuarios sin client_id o con client_id incorrecto
        users_without_client = User.query.filter((User.client_id == None) | (User.client_id == 0)).all()
        users_with_invalid_client = []
        
        all_users = User.query.all()
        for user in all_users:
            client = Client.query.get(user.client_id)
            if not client:
                users_with_invalid_client.append(user)
        
        print(f"Usuarios sin client_id: {len(users_without_client)}")
        print(f"Usuarios con client_id inválido: {len(users_with_invalid_client)}")
        
        # Reparar usuarios sin client_id
        for user in users_without_client:
            print(f"Reparando usuario {user.username} - asignando client_id: {system_client.id}")
            user.client_id = system_client.id
        
        # Reparar usuarios con client_id inválido
        for user in users_with_invalid_client:
            print(f"Reparando usuario {user.username} - client_id inválido {user.client_id}, asignando: {system_client.id}")
            user.client_id = system_client.id
        
        if users_without_client or users_with_invalid_client:
            db.session.commit()
            print("✅ Base de datos reparada correctamente")
        else:
            print("✅ No se encontraron problemas en la base de datos")
        
        print("=== REPARACIÓN COMPLETADA ===")

if __name__ == '__main__':
    fix_database()