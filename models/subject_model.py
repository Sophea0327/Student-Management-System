from models.db import get_db

class SubjectModel:
    """Model for managing subjects with many-to-many teacher assignments."""

    # ------------------------
    # 🔍 READ ALL SUBJECTS WITH TEACHERS
    # ------------------------
    @staticmethod
    def get_all():
        """Fetch all subjects with related class and assigned teachers."""
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                s.id AS subject_id,
                s.name AS subject_name,
                s.image AS subject_image,
                c.name AS class_name,
                GROUP_CONCAT(u.username SEPARATOR ', ') AS teacher_name
            FROM subjects s
            LEFT JOIN classes c ON s.class_id = c.id
            LEFT JOIN subject_teacher st ON s.id = st.subject_id
            LEFT JOIN teachers t ON st.teacher_id = t.id
            LEFT JOIN users u ON t.user_id = u.id
            GROUP BY s.id, s.name, s.image, c.name
            ORDER BY s.id DESC
        """)
        data = cursor.fetchall()
        cursor.close()
        return data
    
    
    @staticmethod
    def get_all_subject_teacher():
        """Fetch all subjects with related class and assigned teachers including assignment metadata."""
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                s.id AS subject_id,
                s.name AS subject_name,
                s.image AS subject_image,
                c.name AS class_name,
                st.id AS assignment_id,
                st.teacher_id,
                st.assigned_at,
                GROUP_CONCAT(u.username SEPARATOR ', ') AS teacher_name
            FROM subjects s
            LEFT JOIN classes c ON s.class_id = c.id
            LEFT JOIN subject_teacher st ON s.id = st.subject_id
            LEFT JOIN teachers t ON st.teacher_id = t.id
            LEFT JOIN users u ON t.user_id = u.id
            GROUP BY s.id, s.name, s.image, c.name, st.id, st.teacher_id, st.assigned_at
            ORDER BY s.id DESC
        """)
        data = cursor.fetchall()
        cursor.close()
        return data
    

    # ------------------------
    # 🔍 GET SUBJECT BY ID WITH TEACHERS
    # ------------------------
    @staticmethod
    def get_by_id(subject_id):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                s.id AS subject_id,
                s.name AS subject_name,
                s.image AS subject_image,
                c.name AS class_name,
                GROUP_CONCAT(u.username SEPARATOR ', ') AS teacher_name
            FROM subjects s
            LEFT JOIN classes c ON s.class_id = c.id
            LEFT JOIN subject_teacher st ON s.id = st.subject_id
            LEFT JOIN teachers t ON st.teacher_id = t.id
            LEFT JOIN users u ON t.user_id = u.id
            WHERE s.id = %s
            GROUP BY s.id, s.name, s.image, c.name
        """, (subject_id,))
        data = cursor.fetchone()
        cursor.close()
        return data

    # ------------------------
    # 🧩 CREATE SUBJECT
    # ------------------------
    @staticmethod
    def add(name, class_id, image=None):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("""
                INSERT INTO subjects (name, class_id, image)
                VALUES (%s, %s, %s)
            """, (name, class_id, image))
            db.commit()
            print(f"✅ Subject '{name}' added successfully.")
        except Exception as e:
            db.rollback()
            print(f"❌ Error adding subject: {e}")
        finally:
            cursor.close()

    # ------------------------
    # ✏️ UPDATE SUBJECT
    # ------------------------
    @staticmethod
    def update(subject_id, name=None, class_id=None, image=None):
        db = get_db()
        cursor = db.cursor()
        try:
            updates = []
            params = []
            if name:
                updates.append("name = %s")
                params.append(name)
            if class_id:
                updates.append("class_id = %s")
                params.append(class_id)
            if image:
                updates.append("image = %s")
                params.append(image)
            if not updates:
                print("⚠️ No fields to update for subject.")
                return
            query = f"UPDATE subjects SET {', '.join(updates)} WHERE id = %s"
            params.append(subject_id)
            cursor.execute(query, tuple(params))
            db.commit()
            print(f"✅ Subject ID {subject_id} updated successfully.")
        except Exception as e:
            db.rollback()
            print(f"❌ Error updating subject: {e}")
        finally:
            cursor.close()

    # ------------------------
    # 👩‍🏫 ASSIGN TEACHER
    # ------------------------
    @staticmethod
    def assign_teacher_to_subject(subject_id, teacher_id):
        """Assign a teacher to a subject."""
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("""
                INSERT INTO subject_teacher (subject_id, teacher_id, assigned_at)
                VALUES (%s, %s, NOW())
            """, (subject_id, teacher_id))
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
        finally:
            cursor.close()
    # ------------------------
    # 👩‍🏫 REMOVE TEACHER ASSIGNMENT
    # ------------------------
    @staticmethod
    def remove_teacher(subject_id, teacher_id):
        """Remove a teacher assignment from a subject."""
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("""
                DELETE FROM subject_teacher
                WHERE subject_id = %s AND teacher_id = %s
            """, (subject_id, teacher_id))
            db.commit()
            print(f"🗑️ Removed teacher ID {teacher_id} from subject ID {subject_id}.")
        except Exception as e:
            db.rollback()
            print(f"❌ Error removing teacher: {e}")
        finally:
            cursor.close()

    # ------------------------
    # ❌ DELETE SUBJECT
    # ------------------------
    @staticmethod
    def delete(subject_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM subjects WHERE id = %s", (subject_id,))
            db.commit()
            print(f"🗑️ Subject ID {subject_id} deleted successfully.")
        except Exception as e:
            db.rollback()
            print(f"❌ Error deleting subject: {e}")
        finally:
            cursor.close()
