import mysql.connector
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

def seed_data():
    conn = mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )
    cursor = conn.cursor()

    print("⚙️ Resetting and seeding data...")

    # ------------------------------------------------
    # 🔹 Step 1: Clean all tables before inserting data
    # ------------------------------------------------
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    tables = [
        'subject_teacher',
        'audit_logs',
        'grades',
        'attendance',
        'subjects',
        'students',
        'classes',
        'teachers',
        'users'
    ]
    for t in tables:
        cursor.execute(f"TRUNCATE TABLE {t};")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    # ------------------------------------------------
    # 🔹 Step 2: Insert users (added image)
    # ------------------------------------------------
    cursor.execute("""
    INSERT INTO users (username, email, password_hash, role, image, status)
    VALUES
    ('admin', 'admin@example.com', '$pbkdf2:sha256:600000$admin$1234567890abcdef', 'admin', 'images/users/admin.jpg', 'active'),
    ('teacher1', 'teacher1@example.com', '$pbkdf2:sha256:600000$teacher1$abcdef1234567890', 'teacher', 'images/users/teacher1.jpg', 'active'),
    ('teacher2', 'teacher2@example.com', '$pbkdf2:sha256:600000$teacher2$fedcba0987654321', 'teacher', 'images/users/teacher2.jpg', 'active');
    """)

    # Get user IDs dynamically
    cursor.execute("SELECT id, username FROM users")
    user_map = {name: uid for uid, name in cursor.fetchall()}

    # ------------------------------------------------
    # 🔹 Step 3: Insert teachers (added image)
    # ------------------------------------------------
    cursor.executemany("""
    INSERT INTO teachers (user_id, name, email, contact, specialization, image, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, [
        (user_map['teacher1'], 'Mr. Dara', 'teacher1@example.com', '0123456789', 'Mathematics', 'images/teachers/dara.jpg', 'active'),
        (user_map['teacher2'], 'Ms. Lina', 'teacher2@example.com', '0987654321', 'Science', 'images/teachers/lina.jpg', 'active'),
    ])

    cursor.execute("SELECT id, name FROM teachers")
    teacher_map = {name: tid for tid, name in cursor.fetchall()}

    # ------------------------------------------------
    # 🔹 Step 4: Insert classes
    # ------------------------------------------------
    cursor.executemany("""
    INSERT INTO classes (name, year, teacher_id)
    VALUES (%s, %s, %s)
    """, [
        ('Class A', 2025, teacher_map['Mr. Dara']),
        ('Class B', 2025, teacher_map['Ms. Lina']),
    ])

    cursor.execute("SELECT id, name FROM classes")
    class_map = {name: cid for cid, name in cursor.fetchall()}

    # ------------------------------------------------
    # 🔹 Step 5: Insert students
    # ------------------------------------------------
    cursor.executemany("""
    INSERT INTO students (name, gender, dob, email, contact, address, image, class_id, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, [
        ('John Doe', 'Male', '2008-03-12', 'john.doe@studentmail.com', '0123456789', 'Phnom Penh', 'images/students/john.jpg', class_map['Class A'], 'active'),
        ('Lisa Chan', 'Female', '2008-06-25', 'lisa.chan@studentmail.com', '0987654321', 'Siem Reap', 'images/students/lisa.jpg', class_map['Class A'], 'active'),
        ('Mark Lim', 'Male', '2009-01-15', 'mark.lim@studentmail.com', '011223344', 'Battambang', 'images/students/mark.jpg', class_map['Class B'], 'active'),
        ('Sophy Eng', 'Female', '2009-04-10', 'sophy.eng@studentmail.com', '099887766', 'Kampot', 'images/students/sophy.jpg', class_map['Class B'], 'active'),
    ])

    cursor.execute("SELECT id, name FROM students")
    student_map = {name: sid for sid, name in cursor.fetchall()}

    # ------------------------------------------------
    # 🔹 Step 6: Insert subjects
    # ------------------------------------------------
    cursor.executemany("""
    INSERT INTO subjects (name, image, class_id)
    VALUES (%s, %s, %s)
    """, [
        ('Mathematics', 'images/subjects/math.png', class_map['Class A']),
        ('Science', 'images/subjects/science.png', class_map['Class A']),
        ('English', 'images/subjects/english.png', class_map['Class B']),
        ('History', 'images/subjects/history.png', class_map['Class B']),
    ])

    cursor.execute("SELECT id, name FROM subjects")
    subject_map = {name: sid for sid, name in cursor.fetchall()}

    # ------------------------------------------------
    # 🔹 Step 7: Assign teachers to subjects
    # ------------------------------------------------
    cursor.executemany("""
    INSERT INTO subject_teacher (subject_id, teacher_id)
    VALUES (%s, %s)
    """, [
        (subject_map['Mathematics'], teacher_map['Mr. Dara']),
        (subject_map['Science'], teacher_map['Ms. Lina']),
        (subject_map['English'], teacher_map['Mr. Dara']),
        (subject_map['History'], teacher_map['Ms. Lina']),
    ])

    # ------------------------------------------------
    # 🔹 Step 8: Insert attendance
    # ------------------------------------------------
    cursor.executemany("""
    INSERT INTO attendance (student_id, class_id, date, status)
    VALUES (%s, %s, %s, %s)
    """, [
        (student_map['John Doe'], class_map['Class A'], '2025-10-25', 'Present'),
        (student_map['Lisa Chan'], class_map['Class A'], '2025-10-25', 'Absent'),
        (student_map['Mark Lim'], class_map['Class B'], '2025-10-25', 'Late'),
        (student_map['Sophy Eng'], class_map['Class B'], '2025-10-25', 'Present'),
    ])

    # ------------------------------------------------
    # 🔹 Step 9: Insert grades
    # ------------------------------------------------
    cursor.executemany("""
    INSERT INTO grades (student_id, subject_id, class_id, teacher_id, term, score, grade_letter, remarks)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, [
        (student_map['John Doe'], subject_map['Mathematics'], class_map['Class A'], teacher_map['Mr. Dara'], 'Term 1', 85.50, 'B', 'Good understanding'),
        (student_map['John Doe'], subject_map['Science'], class_map['Class A'], teacher_map['Ms. Lina'], 'Term 1', 90.00, 'A', 'Excellent work'),
        (student_map['Lisa Chan'], subject_map['Mathematics'], class_map['Class A'], teacher_map['Mr. Dara'], 'Term 1', 78.25, 'C', 'Needs improvement'),
        (student_map['Mark Lim'], subject_map['English'], class_map['Class B'], teacher_map['Mr. Dara'], 'Term 1', 88.75, 'B+', 'Strong performance'),
        (student_map['Sophy Eng'], subject_map['History'], class_map['Class B'], teacher_map['Ms. Lina'], 'Term 1', 92.00, 'A', 'Outstanding result'),
    ])

    # ------------------------------------------------
    # 🔹 Step 10: Insert audit logs
    # ------------------------------------------------
    cursor.executemany("""
    INSERT INTO audit_logs (user_id, action)
    VALUES (%s, %s)
    """, [
        (user_map['admin'], 'Created initial setup and user accounts'),
        (user_map['teacher1'], 'Assigned Class A and uploaded grades'),
        (user_map['teacher2'], 'Marked attendance for Class B'),
    ])

    # ------------------------------------------------
    # 🔹 Finalize
    # ------------------------------------------------
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ All data seeded successfully with image paths and subject-teacher assignments!")

if __name__ == "__main__":
    seed_data()
