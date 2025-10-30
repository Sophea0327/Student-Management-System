from models.db import get_db

class GradeModel:
    """Model for managing student grades."""

    @staticmethod
    def get_all_grades():
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                g.id,
                s.username AS student_name,
                sub.name AS subject_name,
                c.name AS class_name,
                g.score,
                g.grade_letter,
                g.remarks
            FROM grades g
            JOIN students st ON g.student_id = st.id
            JOIN users s ON st.id = s.id
            JOIN subjects sub ON g.subject_id = sub.id
            JOIN classes c ON g.class_id = c.id
            ORDER BY s.username ASC
        """)
        grades = cursor.fetchall()
        cursor.close()
        return grades

    @staticmethod
    def add_grade(student_id, subject_id, class_id, score, grade, remarks):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO grades (student_id, subject_id, class_id, score, grade_letter, remarks)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (student_id, subject_id, class_id, score, grade, remarks))
        db.commit()
        cursor.close()

    @staticmethod
    def get_grade_by_id(grade_id):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                g.id,
                g.score,
                g.grade_letter,
                g.remarks,
                s.username AS student_name,
                sub.name AS subject_name,
                c.name AS class_name
            FROM grades g
            JOIN students st ON g.student_id = st.id
            JOIN users s ON st.id = s.id
            JOIN subjects sub ON g.subject_id = sub.id
            JOIN classes c ON g.class_id = c.id
            WHERE g.id = %s
        """, (grade_id,))
        grade = cursor.fetchone()
        cursor.close()
        return grade


    @staticmethod
    def update_grade(grade_id, score, grade, remarks):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE grades
            SET score = %s, grade_letter = %s, remarks = %s
            WHERE id = %s
        """, (score, grade, remarks, grade_id))
        db.commit()
        cursor.close()

    @staticmethod
    def delete_grade(grade_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM grades WHERE id = %s", (grade_id,))
        db.commit()
        cursor.close()
