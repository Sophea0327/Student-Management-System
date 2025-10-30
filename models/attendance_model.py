# ==============================================================
# FILE: models/attendance_model.py
# PURPOSE: Manage attendance-related database operations
# AUTHOR: Chandy Neat
# ==============================================================

import mysql.connector
from mysql.connector import Error
from config import Config


class AttendanceModel:
    # --------------------------------------------------------------
    # ✅ Helper: Connect to Database
    # --------------------------------------------------------------
    @staticmethod
    def get_connection():
        try:
            conn = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB
            )
            return conn
        except Error as e:
            print(f"❌ Database connection error: {e}")
            return None

    # --------------------------------------------------------------
    # ✅ Get all attendance records with student & class info
    # --------------------------------------------------------------
    @staticmethod
    def get_all_attendance():
        conn = AttendanceModel.get_connection()
        if not conn:
            return []

        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                a.id, 
                s.name AS student_name, 
                c.name AS class_name, 
                a.date, 
                a.status
            FROM attendance a
            JOIN students s ON a.student_id = s.id
            JOIN classes c ON a.class_id = c.id
            ORDER BY a.date DESC;
        """)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    # --------------------------------------------------------------
    # ✅ Get attendance by class
    # --------------------------------------------------------------
    @staticmethod
    def get_attendance_by_class(class_id):
        conn = AttendanceModel.get_connection()
        if not conn:
            return []

        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                a.id,
                s.name AS student_name,
                c.name AS class_name,
                a.date,
                a.status
            FROM attendance a
            JOIN students s ON a.student_id = s.id
            JOIN classes c ON a.class_id = c.id
            WHERE a.class_id = %s
            ORDER BY a.date DESC;
        """, (class_id,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    # --------------------------------------------------------------
    # ✅ Get all students in a specific class
    # --------------------------------------------------------------
    @staticmethod
    def get_students_in_class(class_id):
        conn = AttendanceModel.get_connection()
        if not conn:
            return []

        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, name 
            FROM students 
            WHERE class_id = %s AND status = 'active';
        """, (class_id,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    # --------------------------------------------------------------
    # ✅ Mark attendance (insert or update)
    # --------------------------------------------------------------
    @staticmethod
    def mark_attendance(student_id, class_id, date, status):
        conn = AttendanceModel.get_connection()
        if not conn:
            return

        cursor = conn.cursor()

        # Check if attendance exists for this student & date
        cursor.execute("""
            SELECT id FROM attendance 
            WHERE student_id = %s AND date = %s;
        """, (student_id, date))
        existing = cursor.fetchone()

        if existing:
            cursor.execute("""
                UPDATE attendance 
                SET status = %s, class_id = %s
                WHERE student_id = %s AND date = %s;
            """, (status, class_id, student_id, date))
        else:
            cursor.execute("""
                INSERT INTO attendance (student_id, class_id, date, status)
                VALUES (%s, %s, %s, %s);
            """, (student_id, class_id, date, status))

        conn.commit()
        cursor.close()
        conn.close()

    # --------------------------------------------------------------
    # ✅ Get attendance summary for a student
    # --------------------------------------------------------------
    @staticmethod
    def get_student_summary(student_id):
        conn = AttendanceModel.get_connection()
        if not conn:
            return None

        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                COUNT(*) AS total_classes,
                SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) AS total_present,
                SUM(CASE WHEN status = 'Absent' THEN 1 ELSE 0 END) AS total_absent,
                SUM(CASE WHEN status = 'Late' THEN 1 ELSE 0 END) AS total_late,
                SUM(CASE WHEN status = 'Excused' THEN 1 ELSE 0 END) AS total_excused
            FROM attendance
            WHERE student_id = %s;
        """, (student_id,))
        summary = cursor.fetchone()
        cursor.close()
        conn.close()
        return summary
