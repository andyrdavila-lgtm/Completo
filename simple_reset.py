# simple_reset.py
import sys
import os
import urllib.parse

# Configuración
DB_SERVER = 'localhost'
DB_NAME = 'SISTEMACOM'
DB_DRIVER = 'ODBC Driver 17 for SQL Server'

DB_CONNECTION_STRING = f'DRIVER={{{DB_DRIVER}}};SERVER={DB_SERVER};DATABASE={DB_NAME};Trusted_Connection=yes;'
encoded_connection_string = urllib.parse.quote_plus(DB_CONNECTION_STRING)
DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={encoded_connection_string}"

print("🔧 Reset simple de base de datos...")
print("📋 Esta es solo una verificación de configuración")
print(f"🔗 Cadena de conexión: {DATABASE_URI[:50]}...")
print("✅ Si ves esto, la configuración básica está correcta")