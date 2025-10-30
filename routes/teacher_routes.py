# routes/teacher_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from models.teacher_model import TeacherModel

teacher_routes = Blueprint('teacher_routes', __name__)

@teacher_routes.route('/teachers')
def teachers():
    if 'role' not in session or session['role'] != 'admin':
        flash("Access denied: Admins only", "danger")
        return redirect(url_for('auth.login'))

    data = TeacherModel.get_all_teachers()
    return render_template('teachers/teachers.html', teachers=data)


@teacher_routes.route('/teachers/add', methods=['POST'])
def add_teacher():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    department = request.form.get('specialization')

    if not all([username, email, password, department]):
        flash("All fields are required", "danger")
        return redirect(url_for('teacher_routes.teachers'))

    password_hash = generate_password_hash(password)
    TeacherModel.add_teacher(username, email, password_hash, department)

    flash("Teacher added successfully!", "success")
    return redirect(url_for('teacher_routes.teachers'))


@teacher_routes.route('/teachers/delete/<int:teacher_id>')
def delete_teacher(teacher_id):
    TeacherModel.delete_teacher(teacher_id)
    flash("Teacher deleted successfully!", "warning")
    return redirect(url_for('teacher_routes.teachers'))


@teacher_routes.route('/teachers/edit/<int:teacher_id>', methods=['POST'])
def edit_teacher(teacher_id):
    username = request.form.get('username')
    email = request.form.get('email')
    department = request.form.get('department')

    TeacherModel.update_teacher(teacher_id, username, email, department)
    flash("Teacher updated successfully!", "info")
    return redirect(url_for('teacher_routes.teachers'))
