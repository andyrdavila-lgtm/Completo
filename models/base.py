# models/base.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# --- Tablas de Asociación para Roles y Permisos ---

# Tabla para la relación muchos a muchos entre Roles y Permisos
roles_permissions = db.Table('roles_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)

# Tabla para la relación muchos a muchos entre Usuarios y Roles
users_roles = db.Table('users_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

    # Relación muchos a muchos con Permisos
    permissions = db.relationship('Permission', secondary=roles_permissions, back_populates='roles')

    def __repr__(self):
        return f'<Role {self.name}>'

class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False) # ej: 'dashboard.view', 'users.create'
    description = db.Column(db.String(255))

    # Relación inversa con Roles
    roles = db.relationship('Role', secondary=roles_permissions, back_populates='permissions')

    def __repr__(self):
        return f'<Permission {self.name}>'


class BusinessType(db.Model):
    __tablename__ = 'business_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    clients = db.relationship('Client', back_populates='business_type')

    def __repr__(self):
        return f'<BusinessType {self.name}>'

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    business_type_id = db.Column(db.Integer, db.ForeignKey('business_types.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    business_type = db.relationship('BusinessType', back_populates='clients')
    users = db.relationship('User', back_populates='client')

    def __repr__(self):
        return f'<Client {self.name}>'

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    # El campo 'role' se mantiene para una distinción rápida (superadmin/user),
    # pero los permisos granulares vienen de los roles.
    role = db.Column(db.String(20), default='user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))

    client = db.relationship('Client', back_populates='users')

    # Relación muchos a muchos con Roles
    roles = db.relationship('Role', secondary=users_roles, backref=db.backref('users', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission_name):
        """Verifica si el usuario tiene un permiso específico a través de sus roles."""
        if self.role == 'superadmin':
            return True
        for role in self.roles:
            for permission in role.permissions:
                if permission.name == permission_name:
                    return True
        return False

    def __repr__(self):
        return f'<User {self.username}>'