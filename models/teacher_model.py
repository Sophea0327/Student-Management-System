from models.db import get_db

class TeacherModel:
    """Model for managing teacher-related operations."""

    # ------------------------
    # 🔍 READ OPERATIONS
    # ------------------------
    @staticmethod
    def get_all_teachers():
        """Fetch all teachers with user info."""
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                u.id, u.username, u.email, u.image, u.status, 
                t.specialization
            FROM teachers t
            JOIN users u ON t.user_id = u.id
            ORDER BY u.username ASC
        """)
        data = cursor.fetchall()
        cursor.close()
        return data

    @staticmethod
    def get_teacher_by_id(teacher_id):
        """Fetch a single teacher by user ID."""
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                u.id, u.username, u.email, u.image, 
                t.specialization, u.status
            FROM teachers t
            JOIN users u ON t.user_id = u.id
            WHERE u.id = %s
        """, (teacher_id,))
        data = cursor.fetchone()
        cursor.close()
        return data

    # ------------------------
    # 🧩 CREATE
    # ------------------------
    @staticmethod
    def add_teacher(username, email, password_hash, department, image=None):
        """
        Add a new teacher.
        - Inserts into 'users' and 'teachers' tables.
        - Optional image path can be passed.
        """
        db = get_db()
        cursor = db.cursor()

        try:
            # Insert into users table
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, role, image)
                VALUES (%s, %s, %s, 'teacher', %s)
            """, (username, email, password_hash, image))
            user_id = cursor.lastrowid

            # Insert into teachers table
            cursor.execute("""
                INSERT INTO teachers (user_id, specialization)
                VALUES (%s, %s)
            """, (user_id, department))

            db.commit()
            print(f"✅ Teacher '{username}' added successfully.")
        except Exception as e:
            db.rollback()
            print(f"❌ Error adding teacher: {e}")
        finally:
            cursor.close()

    # ------------------------
    # ✏️ UPDATE
    # ------------------------
    @staticmethod
    def update_teacher(teacher_id, username=None, email=None, department=None, image=None):
        """
        Update teacher and user info.
        Only updates fields provided (non-None values).
        """
        db = get_db()
        cursor = db.cursor()
        try:
            updates = []
            params = []

            if username:
                updates.append("u.username = %s")
                params.append(username)
            if email:
                updates.append("u.email = %s")
                params.append(email)
            if department:
                updates.append("t.specialization = %s")
                params.append(department)
            if image:
                updates.append("u.image = %s")
                params.append(image)

            if not updates:
                print("⚠️ No fields to update for teacher.")
                return

            query = f"""
                UPDATE users u
                JOIN teachers t ON u.id = t.user_id
                SET {', '.join(updates)}
                WHERE u.id = %s
            """
            params.append(teacher_id)
            cursor.execute(query, tuple(params))
            db.commit()
            print(f"✅ Teacher ID {teacher_id} updated successfully.")
        except Exception as e:
            db.rollback()
            print(f"❌ Error updating teacher: {e}")
        finally:
            cursor.close()

    # ------------------------
    # ❌ DELETE
    # ------------------------
    @staticmethod
    def delete_teacher(teacher_id):
        """Delete a teacher and the corresponding user record."""
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM teachers WHERE user_id = %s", (teacher_id,))
            cursor.execute("DELETE FROM users WHERE id = %s", (teacher_id,))
            db.commit()
            print(f"🗑️ Teacher ID {teacher_id} deleted successfully.")
        except Exception as e:
            db.rollback()
            print(f"❌ Error deleting teacher: {e}")
        finally:
            cursor.close()
