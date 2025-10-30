from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.grade_model import GradeModel
from models.student_model import StudentModel
from models.subject_model import SubjectModel
from models.class_model import ClassModel

grade_bp = Blueprint('grade', __name__, url_prefix='/grades')

@grade_bp.route('/')
def list_grades():
    grades = GradeModel.get_all_grades()
    return render_template('grade/grades.html', grades=grades)

@grade_bp.route('/add', methods=['GET', 'POST'])
def add_grade():
    if request.method == 'POST':
        student_id = request.form['student_id']
        subject_id = request.form['subject_id']
        class_id = request.form['class_id']
        score = float(request.form['score'])

        # Grade logic
        if score >= 90:
            grade = 'A'
            remarks = 'Excellent'
        elif score >= 80:
            grade = 'B'
            remarks = 'Good'
        elif score >= 70:
            grade = 'C'
            remarks = 'Average'
        elif score >= 60:
            grade = 'D'
            remarks = 'Needs Improvement'
        else:
            grade = 'F'
            remarks = 'Fail'

        GradeModel.add_grade(student_id, subject_id, class_id, score, grade, remarks)
        flash('Grade added successfully!', 'success')
        return redirect(url_for('grade.list_grades'))

    students = StudentModel.get_all()
    subjects = SubjectModel.get_all()
    classes = ClassModel.get_all()
    return render_template('grade/grade_add.html', students=students, subjects=subjects, classes=classes)

@grade_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_grade(id):
    grade = GradeModel.get_grade_by_id(id)

    if request.method == 'POST':
        score = float(request.form['score'])
        if score >= 90:
            grade_letter = 'A'
            remarks = 'Excellent'
        elif score >= 80:
            grade_letter = 'B'
            remarks = 'Good'
        elif score >= 70:
            grade_letter = 'C'
            remarks = 'Average'
        elif score >= 60:
            grade_letter = 'D'
            remarks = 'Needs Improvement'
        else:
            grade_letter = 'F'
            remarks = 'Fail'

        GradeModel.update_grade(id, score, grade_letter, remarks)
        flash('Grade updated successfully!', 'success')
        return redirect(url_for('grade.list_grades'))

    return render_template('grade/grade_edit.html', grade=grade)


@grade_bp.route('/delete/<int:id>')
def delete_grade(id):
    GradeModel.delete_grade(id)
    flash('Grade deleted successfully!', 'success')
    return redirect(url_for('grade.list_grades'))
