# Melchizideck S. Osorno
import sqlite3, os

def get_conn(db_path="app_data.db") -> sqlite3.Connection:
    # Ensure directory exists for non-rooted paths
    base = os.path.dirname(db_path)
    if base:
        os.makedirs(base, exist_ok=True)
    # connect with row tuples; set pragmas if you like
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return conn

def purchase_get_conn(db_path = "purchase_data.db") -> sqlite3.Connection:
    # Ensure directory exists for non-rooted paths
    base = os.path.dirname(db_path)
    if base:
        os.makedirs(base, exist_ok=True)
    # connect with row tuples; set pragmas if you like
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return conn