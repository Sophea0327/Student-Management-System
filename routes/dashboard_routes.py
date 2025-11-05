from flask import Blueprint, render_template, session, redirect, url_for, flash
from models.db import get_db
from functools import wraps

dashboard_bp = Blueprint('dashboard', __name__)

############################################
#### Middleware: Authentication
############################################

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


############################################
#### MAIN DASHBOARD ENTRY
############################################
@dashboard_bp.route('/')
@login_required
def dashboard_home():
    """Automatically redirect user to their role-based dashboard"""
    role = session.get('role')
    if role == 'admin':
        return redirect(url_for('dashboard.admin_dashboard'))
    elif role == 'teacher':
        return redirect(url_for('dashboard.teacher_dashboard'))
    elif role == 'student':
        return redirect(url_for('dashboard.student_dashboard'))
    else:
        flash("Invalid role. Please contact the system administrator.", "danger")
        return redirect(url_for('auth.logout'))


############################################
#### ADMIN DASHBOARD
############################################
@dashboard_bp.route('/admin')
@login_required
def admin_dashboard():
    if session.get('role') != 'admin':
        flash("You are not authorized to access the admin dashboard.", "danger")
        return redirect(url_for('dashboard.dashboard_home'))

    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        # ---- Stats ----
        cursor.execute("SELECT COUNT(*) AS total_students FROM students")
        total_students = cursor.fetchone()['total_students']

        cursor.execute("SELECT COUNT(*) AS total_teachers FROM users WHERE role='teacher'")
        total_teachers = cursor.fetchone()['total_teachers']

        cursor.execute("SELECT COUNT(*) AS total_classes FROM classes")
        total_classes = cursor.fetchone()['total_classes']

        # ---- Average Grade by Class ----
        cursor.execute("""
            SELECT c.name AS class_name, 
                   ROUND(AVG(g.score), 2) AS avg_score
            FROM grades g
            JOIN classes c ON g.class_id = c.id
            GROUP BY c.name
            ORDER BY c.name
        """)
        class_data = cursor.fetchall()

        class_names = [row['class_name'] for row in class_data]
        avg_grades = [row['avg_score'] for row in class_data]

        # ---- Grade Distribution ----
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
        grade_dist = cursor.fetchall()

        student_labels = [row['grade_category'] for row in grade_dist]
        student_counts = [row['total'] for row in grade_dist]

        return render_template(
            'dashboard/dashboard_admin.html',
            total_students=total_students,
            total_teachers=total_teachers,
            total_classes=total_classes,
            class_names=class_names,
            avg_grades=avg_grades,
            student_labels=student_labels,
            student_counts=student_counts
        )

    except Exception as e:
        print("Admin Dashboard Error:", e)
        flash("Error loading admin dashboard.", "danger")
        return render_template('errors/404.html', message=f"Error: {e}")
    finally:
        cursor.close()
        db.close()


############################################
#### TEACHER DASHBOARD
############################################
@dashboard_bp.route('/teacher')
@login_required
def teacher_dashboard():
    # Only allow teachers
    if session.get('role') != 'teacher':
        flash("Access denied. Teacher only.", "danger")
        return redirect(url_for('dashboard.dashboard_home'))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        teacher_id = session.get('id')

        # ✅ Total Subjects taught by this teacher
        cursor.execute("SELECT COUNT(*) AS total_subjects FROM subjects WHERE id = %s", (teacher_id,))
        total_subjects = cursor.fetchone()['total_subjects'] or 0

        # ✅ Total Students in teacher's classes
        cursor.execute("""
            SELECT COUNT(DISTINCT s.id) AS total_students
            FROM students s
            JOIN classes c ON s.class_id = c.id
            WHERE c.id = %s
        """, (teacher_id,))
        total_students = cursor.fetchone()['total_students'] or 0

        # ✅ Average score overall for this teacher’s classes
        cursor.execute("""
            SELECT ROUND(AVG(g.score), 2) AS overall_avg
            FROM grades g
            JOIN classes c ON g.class_id = c.id
            WHERE c.id = %s
        """, (teacher_id,))
        overall_avg = cursor.fetchone()['overall_avg'] or 0

        # ✅ Chart Data: Average score by class
        cursor.execute("""
            SELECT c.name AS class_name, ROUND(AVG(g.score), 2) AS avg_score
            FROM grades g
            JOIN classes c ON g.class_id = c.id
            WHERE c.id = %s
            GROUP BY c.name
            ORDER BY c.name
        """, (teacher_id,))
        data = cursor.fetchall()

        class_names = [row['class_name'] for row in data] if data else []
        avg_scores = [row['avg_score'] for row in data] if data else []

        # ✅ Render template safely
        return render_template(
            'dashboard/dashboard_teacher.html',
            total_subjects=total_subjects,
            total_students=total_students,
            overall_avg=overall_avg,
            class_names=class_names,
            avg_scores=avg_scores
        )

    except Exception as e:
        print("Teacher Dashboard Error:", e)
        flash("Error loading teacher dashboard.", "danger")
        return render_template('errors/404.html', message=str(e))

    finally:
        cursor.close()
        db.close()


############################################
#### STUDENT DASHBOARD
############################################
@dashboard_bp.route('/student')
@login_required
def student_dashboard():
    if session.get('role') != 'student':
        flash("Access denied: Only students can view this dashboard.", "danger")
        return redirect(url_for('dashboard.dashboard_home'))

    db = get_db()
    cursor = db.cursor(dictionary=True)
    student_id = session.get('id')

    try:
        # Fetch student info
        cursor.execute("SELECT name FROM students WHERE id = %s", (student_id,))
        student_info = cursor.fetchone()
        student_name = student_info['name'] if student_info else "Unknown"

        # Fetch student's grades by subject
        cursor.execute("""
            SELECT s.name AS subject_name, g.score
            FROM grades g
            JOIN subjects s ON g.subject_id = s.id
            WHERE g.student_id = %s
        """, (student_id,))
        grades_data = cursor.fetchall() or []
        labels = [row['subject_name'] for row in grades_data]
        values = [row['score'] for row in grades_data]

        # Attendance count
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END) AS present_days,
                SUM(CASE WHEN status='Absent' THEN 1 ELSE 0 END) AS absent_days
            FROM attendance
            WHERE student_id = %s
        """, (student_id,))
        attendance = cursor.fetchone() or {}
        present_days = attendance.get('present_days', 0)
        absent_days = attendance.get('absent_days', 0)

        return render_template(
            'dashboard/dashboard_student.html',
            student_name=student_name,
            labels=labels,
            values=values,
            present_days=present_days,
            absent_days=absent_days
        )

    except Exception as e:
        print("Student Dashboard Error:", e)
        return render_template('errors/404.html', message=f"Error: {e}")

    finally:
        cursor.close()
        db.close()
