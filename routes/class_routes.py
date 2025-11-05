# ==============================================================
# FILE: routes/classes.py
# DESCRIPTION: Class management routes
# ==============================================================
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from models.class_model import ClassModel
from models.users_model import UserModel

# Blueprint
classes_bp = Blueprint('classes', __name__, url_prefix='/classes')

# ---------------- Middleware: Require login ----------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

# ---------------- Middleware: Require admin ----------------
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'admin':
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for('dashboard.dashboard_home'))
        return f(*args, **kwargs)
    return decorated

# ---------------- List All Classes ----------------
@classes_bp.route('/manage')
def manage_classes():
    classes = ClassModel.get_all()
    return render_template('classes/manage_class.html', classes=classes)

# ---------------- Add New Class ----------------
@classes_bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_class():
    # Get list of teachers for assignment
    teachers = UserModel.get_all_users(role='teacher')
    if request.method == 'POST':
        name = request.form.get('name')
        year = request.form.get('year')
        teacher_id = request.form.get('teacher_id') or None

        if not name or not year:
            flash("⚠️ Name and Year are required.", "warning")
        else:
            success = ClassModel.add(name, year, teacher_id)
            if success:
                flash(f"✅ Class '{name}' created successfully!", "success")
                return redirect(url_for('classes.manage_classes'))
            else:
                flash("❌ Failed to create class.", "danger")

    return render_template('classes/create_class.html', teachers=teachers)

# ---------------- Update Class ----------------
@classes_bp.route('/update/<int:class_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def update_class(class_id):
    class_ = ClassModel.get_by_id(class_id)
    if not class_:
        flash("Class not found.", "danger")
        return redirect(url_for('classes.manage_classes'))

    teachers = UserModel.get_all_users(role='teacher')

    if request.method == 'POST':
        name = request.form.get('name')
        year = request.form.get('year')
        teacher_id = request.form.get('teacher_id') or None

        success = ClassModel.update(class_id, name, year, teacher_id)
        if success:
            flash(f"✅ Class '{name}' updated successfully!", "success")
            return redirect(url_for('classes.manage_classes'))
        else:
            flash("❌ Failed to update class.", "danger")

    return render_template('classes/update_class.html', class_=class_, teachers=teachers)

# ---------------- Delete Class ----------------
@classes_bp.route('/delete/<int:class_id>', methods=['POST'])
@login_required
@admin_required
def delete_class(class_id):
    success = ClassModel.delete(class_id)
    if success:
        flash("🗑️ Class deleted successfully.", "info")
    else:
        flash("❌ Failed to delete class.", "danger")
    return redirect(url_for('classes.manage_classes'))
