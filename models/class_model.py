from models.db import get_db

class ClassModel:
    """Model for managing class-related operations."""

    # --------------------------------------------------------------
    # ✅ Get all classes with teacher info (full details)
    # --------------------------------------------------------------
    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.*, u.username AS teacher_name
            FROM classes c
            LEFT JOIN users u ON c.teacher_id = u.id
            ORDER BY c.year DESC
        """)
        classes = cursor.fetchall()
        cursor.close()
        return classes

    # --------------------------------------------------------------
    # ✅ Get simplified list of all classes (id + name)
    # --------------------------------------------------------------
    @staticmethod
    def get_all_classes():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, name, year
            FROM classes
            ORDER BY year DESC, name ASC
        """)
        classes = cursor.fetchall()
        cursor.close()
        return classes

    # --------------------------------------------------------------
    # ✅ Add a new class
    # --------------------------------------------------------------
    @staticmethod
    def add(name, year, teacher_id=None):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO classes (name, year, teacher_id) 
            VALUES (%s, %s, %s)
        """, (name, year, teacher_id))
        db.commit()
        cursor.close()

    # --------------------------------------------------------------
    # ✅ Delete a class by ID
    # --------------------------------------------------------------
    @staticmethod
    def delete(class_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM classes WHERE id = %s", (class_id,))
        db.commit()
        cursor.close()
