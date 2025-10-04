# models/__init__.py
from .base import db, BusinessType, Client, User

# Solo importa las clases que realmente existen
__all__ = ['db', 'BusinessType', 'Client', 'User']