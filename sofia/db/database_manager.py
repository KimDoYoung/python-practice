# database_manager.py
from .databases import DatabaseConnection

DATABASE_URL = "sqlite:///c:/tmp/sofia.sqlite"
db_connection = DatabaseConnection(DATABASE_URL)

def get_db_connection():
    return db_connection
