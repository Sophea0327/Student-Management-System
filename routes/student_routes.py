# routes/student_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.student_model import StudentModel
from models.class_model import ClassModel # for selecting classes

student_bp = Blueprint('student', __name__, url_prefix='/students')

@student_bp.route('/')
def list_students():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    students = StudentModel.get_all()
    return render_template('students/students.html', students=students)


@student_bp.route('/add', methods=['GET', 'POST'])
def add_student():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    classes = ClassModel.get_all()

    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        date_of_birth = request.form['date_of_birth']
        address = request.form['address']
        class_id = request.form['class_id']

        StudentModel.add(name, gender, date_of_birth, address, class_id)
        flash('Student added successfully!', 'success')
        return redirect(url_for('student.list_students'))

    return render_template('students/add_student.html', classes=classes)


@student_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    student = StudentModel.get_by_id(id)
    classes = ClassModel.get_all()

    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        date_of_birth = request.form['date_of_birth']
        address = request.form['address']
        class_id = request.form['class_id']

        StudentModel.update(id, name, gender, date_of_birth, address, class_id)
        flash('Student updated successfully!', 'success')
        return redirect(url_for('student.list_students'))

    return render_template('students/edit_student.html', student=student, classes=classes)


@student_bp.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    StudentModel.delete(id)
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('student.list_students'))
