from flask import Blueprint, render_template, session, redirect, url_for
from models.db import get_db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        # ---- Basic Stats ----
        cursor.execute("SELECT COUNT(*) AS total_students FROM students")
        total_students = cursor.fetchone()['total_students']

        cursor.execute("SELECT COUNT(*) AS total_teachers FROM users WHERE role='teacher'")
        total_teachers = cursor.fetchone()['total_teachers']

        cursor.execute("SELECT COUNT(*) AS total_classes FROM classes")
        total_classes = cursor.fetchone()['total_classes']

        # ---- Bar Chart: Average Grade by Class ----
        cursor.execute("""
            SELECT c.name AS class_name, 
                   ROUND(AVG(g.score), 2) AS avg_score
            FROM grades g
            JOIN classes c ON g.class_id = c.id
            GROUP BY c.name
            ORDER BY c.name
        """)
        class_grade_data = cursor.fetchall()
        class_names = [row['class_name'] for row in class_grade_data]
        avg_grades = [row['avg_score'] for row in class_grade_data]

        # ---- Pie Chart: Student Grade Distribution ----
        cursor.execute("""
            SELECT 
                CASE
                    WHEN score >= 90 THEN 'A'
                    WHEN score >= 80 THEN 'B'
                    WHEN score >= 70 THEN 'C'
                    WHEN score >= 60 THEN 'D'
                    ELSE 'F'
                END AS grade_category,
                COUNT(*) AS total
            FROM grades
            GROUP BY grade_category
            ORDER BY grade_category ASC
        """)
        grade_distribution = cursor.fetchall()
        student_labels = [row['grade_category'] for row in grade_distribution]
        student_counts = [row['total'] for row in grade_distribution]

        return render_template(
            'dashboard_admin.html',
            total_students=total_students,
            total_teachers=total_teachers,
            total_classes=total_classes,
            class_names=class_names,
            avg_grades=avg_grades,
            student_labels=student_labels,
            student_counts=student_counts
        )

    except Exception as e:
        print("Dashboard Error:", e)
        return render_template('errors/404.html', message=f"Error: {e}")

    finally:
        cursor.close()
        db.close()