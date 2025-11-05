from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash
)
from models.class_model import ClassModel
from models.subject_model import SubjectModel
from models.db import get_db

subjects_bp = Blueprint('subjects', __name__, url_prefix='/subjects')




# ============================================================
# SUBJECT MANAGEMENT
# ============================================================
@subjects_bp.route('/')
def subject_list():
    subjects = SubjectModel.get_all()
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM classes")
    classes = cursor.fetchall()
    cursor.execute("SELECT id, username FROM users WHERE role='teacher'")
    teachers = cursor.fetchall()
    cursor.close()
    return render_template('subjects/subject_list.html', subjects=subjects, classes=classes, teachers=teachers)



@subjects_bp.route('/add', methods=['POST'])
def add_subject():
    """Add a new subject."""
    name = request.form.get('name')
    class_id = request.form.get('class_id')

    if not name or not class_id:
        flash('⚠️ Please fill all fields!', 'danger')
        return redirect(url_for('subjects.subject_list'))

    SubjectModel.add(name, class_id)
    flash('📚 Subject added successfully!', 'success')
    return redirect(url_for('subjects.subject_list'))


# ============================================================
# ASSIGN TEACHER MANAGEMENT
# ============================================================
@subjects_bp.route('/assign_page', methods=['GET', 'POST'])
def assign_page():
    """
    Render and handle the subject-teacher assignment page.
    Users can assign a teacher to a subject via the HTML form.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        # ---------- Handle Form Submission ----------
        if request.method == 'POST':
            subject_id = request.form.get('subject_id')
            teacher_id = request.form.get('teacher_id')

            if not subject_id or not teacher_id:
                flash('⚠️ Please select both a subject and a teacher before submitting.', 'warning')
            else:
                assigned = SubjectModel.assign_teacher_to_subject(subject_id, teacher_id)

                if assigned:
                    flash('✅ Teacher successfully assigned to subject!', 'success')
                else:
                    flash('❌ Failed to assign teacher. Please try again.', 'danger')

            # Redirect to clear POST data and refresh assignments
            return redirect(url_for('subjects.assign_page'))

        # ---------- Handle Page Load (GET) ----------
        subjects_with_teachers = SubjectModel.get_all_subject_teacher()

        # Fetch dropdown data
        cursor.execute("SELECT id, name FROM classes ORDER BY name ASC")
        classes = cursor.fetchall()

        cursor.execute("""
            SELECT t.id, u.username 
            FROM teachers t
            JOIN users u ON t.user_id = u.id
            ORDER BY u.username ASC
        """)
        teachers = cursor.fetchall()


        return render_template(
            'subjects/assign_page.html',
            subjects=subjects_with_teachers,
            classes=classes,
            teachers=teachers
        )

    except Exception as e:
        flash(f'🚫 An unexpected error occurred: {str(e)}', 'danger')
        return render_template('errors/404.html', message=f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
