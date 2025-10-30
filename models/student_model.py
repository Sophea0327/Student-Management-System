# models/student_model.py
from models.db import get_db

class StudentModel:
    """Model for managing students."""

    # ------------------------
    # 🔍 READ
    # ------------------------
    @staticmethod
    def get_all():
        """Fetch all students with their class info."""
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                s.id, s.name, s.gender, s.dob, s.email, s.contact, s.address,
                s.image, s.status, c.name AS class_name
            FROM students s
            LEFT JOIN classes c ON s.class_id = c.id
            ORDER BY s.id DESC
        """)
        students = cursor.fetchall()
        cursor.close()
        return students

    @staticmethod
    def get_by_id(student_id):
        """Fetch a student by ID."""
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                s.*, c.name AS class_name
            FROM students s
            LEFT JOIN classes c ON s.class_id = c.id
            WHERE s.id = %s
        """, (student_id,))
        student = cursor.fetchone()
        cursor.close()
        return student

    # ------------------------
    # 🧩 CREATE
    # ------------------------
    @staticmethod
    def add(name, gender=None, dob=None, email=None, contact=None, address=None, class_id=None, image=None, status="active"):
        """Add a new student."""
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("""
                INSERT INTO students (name, gender, dob, email, contact, address, class_id, image, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, gender, dob, email, contact, address, class_id, image, status))
            db.commit()
            print(f"✅ Student '{name}' added successfully.")
        except Exception as e:
            db.rollback()
            print(f"❌ Error adding student: {e}")
        finally:
            cursor.close()

    # ------------------------
    # ✏️ UPDATE
    # ------------------------
    @staticmethod
    def update(student_id, name=None, gender=None, dob=None, email=None, contact=None, address=None, class_id=None, image=None, status=None):
        """Update student details (only provided fields)."""
        db = get_db()
        cursor = db.cursor()
        try:
            updates = []
            params = []

            if name:
                updates.append("name = %s")
                params.append(name)
            if gender:
                updates.append("gender = %s")
                params.append(gender)
            if dob:
                updates.append("dob = %s")
                params.append(dob)
            if email:
                updates.append("email = %s")
                params.append(email)
            if contact:
                updates.append("contact = %s")
                params.append(contact)
            if address:
                updates.append("address = %s")
                params.append(address)
            if class_id:
                updates.append("class_id = %s")
                params.append(class_id)
            if image:
                updates.append("image = %s")
                params.append(image)
            if status:
                updates.append("status = %s")
                params.append(status)

            if not updates:
                print("⚠️ No fields provided for update.")
                return

            query = f"UPDATE students SET {', '.join(updates)} WHERE id = %s"
            params.append(student_id)

            cursor.execute(query, tuple(params))
            db.commit()
            print(f"✅ Student ID {student_id} updated successfully.")
        except Exception as e:
            db.rollback()
            print(f"❌ Error updating student: {e}")
        finally:
            cursor.close()

    # ------------------------
    # ❌ DELETE
    # ------------------------
    @staticmethod
    def delete(student_id):
        """Delete a student by ID."""
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            db.commit()
            print(f"🗑️ Student ID {student_id} deleted successfully.")
        except Exception as e:
            db.rollback()
            print(f"❌ Error deleting student: {e}")
        finally:
            cursor.close()
