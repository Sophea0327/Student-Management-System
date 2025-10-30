# models/db.py
import os
import mysql.connector
from flask import current_app, g
from mysql.connector import Error

def get_db():
    """
    Return a MySQL connection from flask.g, using current_app.config.
    Must be called inside app context / request context.
    """
    if 'db' not in g:
        # prefer current_app.config, but fallback to ENV vars (defensive)
        host = current_app.config.get('MYSQL_HOST') or os.getenv('MYSQL_HOST', 'localhost')
        user = current_app.config.get('MYSQL_USER') or os.getenv('MYSQL_USER', 'root')
        password = current_app.config.get('MYSQL_PASSWORD') or os.getenv('MYSQL_PASSWORD', '')
        database = current_app.config.get('MYSQL_DB') or os.getenv('MYSQL_DB', 'student_management')

        try:
            g.db = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                autocommit=False
            )
        except Error as e:
            # raise a clear error so Flask debugger shows it
            raise RuntimeError(f"Could not connect to MySQL: {e}") from e

    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None and getattr(db, 'is_connected', None):
        try:
            if db.is_connected():
                db.close()
        except Exception:
            pass
