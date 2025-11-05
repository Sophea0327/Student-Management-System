# =====================================================================
# FILE: models/user_model.py
# DESCRIPTION: User Model for managing CRUD operations and authentication
# =====================================================================

from .db import get_db
from werkzeug.security import check_password_hash, generate_password_hash
from mysql.connector import Error


class UserModel:

    # ------------------------
    # 🔍 READ OPERATIONS
    # ------------------------
    @staticmethod
    def get_all_users(role=None):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            if role:
                cursor.execute("SELECT * FROM users WHERE role != 'admin'")
            else:
                cursor.execute("SELECT * FROM users")
            return cursor.fetchall()
        finally:
            cursor.close()

   


    @staticmethod
    def get_user_by_id(user_id):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            return cursor.fetchone()
        finally:
            cursor.close()

    @staticmethod
    def get_user_by_email(email):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            return cursor.fetchone()
        finally:
            cursor.close()
    @staticmethod
    def get_user_by_username(username):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            return cursor.fetchone()
        finally:
            cursor.close()

    find_by_username = get_user_by_email  # alias
    find_by_username = get_user_by_username  # alias

    @staticmethod
    def get_user_by_email(email):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            return cursor.fetchone()
        finally:
            cursor.close()

    # ------------------------
    # 🧩 CREATE (expects password already hashed)
    # ------------------------
    @staticmethod
    def create_user(username, email, password_hash, role, status="active", image=None):
        db = get_db()
        cursor = db.cursor()
        try:
            print("Attempting insert:", username, email, role)
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, role, status, image)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (username, email, password_hash, role, status, image))
            db.commit()
            print(f"✅ User '{username}' with role '{role}' created successfully.")
        except Error as e:
            print(f"❌ Error creating user: {e}")
            db.rollback()
        finally:
            cursor.close()



    # ------------------------
    # ✏️ UPDATE (expects password already hashed)
    # ------------------------
    @staticmethod
    def update_user(user_id, username=None, email=None, password=None, role=None, status=None, image=None):
        db = get_db()
        cursor = db.cursor()
        try:
            updates = []
            params = []

            if username:
                updates.append("username = %s")
                params.append(username)
            if email:
                updates.append("email = %s")
                params.append(email)
            if password:  # password must be pre-hashed before calling this
                updates.append("password_hash = %s")
                params.append(password)
            if role:
                updates.append("role = %s")
                params.append(role)
            if status:
                updates.append("status = %s")
                params.append(status)
            if image:
                updates.append("image = %s")
                params.append(image)

            if not updates:
                print("⚠️ No fields to update.")
                return

            query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
            params.append(user_id)
            cursor.execute(query, tuple(params))
            db.commit()
            print(f"✅ User ID {user_id} updated successfully.")
        except Error as e:
            print(f"❌ Error updating user: {e}")
            db.rollback()
        finally:
            cursor.close()

    # ------------------------
    # ❌ DELETE
    # ------------------------
    @staticmethod
    def delete_user(user_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            db.commit()
            print(f"🗑️ User ID {user_id} deleted successfully.")
        except Error as e:
            print(f"❌ Error deleting user: {e}")
            db.rollback()
        finally:
            cursor.close()

    # ------------------------
    # 🔐 AUTH HELPERS
    # ------------------------
    @staticmethod
    def verify_password(stored_hash, password):
        return check_password_hash(stored_hash, password)

    @staticmethod
    def change_password(user_id, new_password):
        db = get_db()
        cursor = db.cursor()
        try:
            hashed = generate_password_hash(new_password)
            cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s", (hashed, user_id))
            db.commit()
            print(f"🔑 Password updated for user ID {user_id}.")
        except Error as e:
            print(f"❌ Error updating password: {e}")
            db.rollback()
        finally:
            cursor.close()

    # ------------------------
    # 📜 STATUS MANAGEMENT
    # ------------------------
    @staticmethod
    def set_user_status(user_id, status):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("UPDATE users SET status = %s WHERE id = %s", (status, user_id))
            db.commit()
            print(f"⚙️ User ID {user_id} status set to '{status}'.")
        except Error as e:
            print(f"❌ Error updating status: {e}")
            db.rollback()
        finally:
            cursor.close()

    # ------------------------
    # 🧾 EXTRA UTILITIES
    # ------------------------
    @staticmethod
    def count_users():
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM users")
            (count,) = cursor.fetchone()
            return count
        finally:
            cursor.close()

    @staticmethod
    def search_users(keyword):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        try:
            like = f"%{keyword}%"
            cursor.execute("""
                SELECT * FROM users
                WHERE username LIKE %s OR email LIKE %s
            """, (like, like))
            return cursor.fetchall()
        finally:
            cursor.close()
