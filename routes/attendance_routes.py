# routes/attendance_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import date
from models.attendance_model import AttendanceModel
from models.class_model import ClassModel

attendance_routes = Blueprint('attendance_routes', __name__)

@attendance_routes.route('/attendance')
def attendance():
    if 'role' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('auth.login'))

    data = AttendanceModel.get_all_attendance()
    classes = ClassModel.get_all_classes()
    return render_template('attendance/attendance.html', attendance=data, classes=classes)

@attendance_routes.route('/attendance/mark', methods=['POST'])
def mark_attendance():
    class_id = request.form.get('class_id')
    statuses = request.form.getlist('status')
    student_ids = request.form.getlist('student_id')

    for student_id, status in zip(student_ids, statuses):
        AttendanceModel.mark_attendance(student_id, date.today(), status)

    flash("Attendance marked successfully!", "success")
    return redirect(url_for('attendance_routes.attendance'))

@attendance_routes.route('/attendance/students/<int:class_id>')
def get_students_by_class(class_id):
    students = AttendanceModel.get_students_in_class(class_id)
    return {'students': students}
