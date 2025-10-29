# ==============================================================
# FILE: migrations/create_tables.py
# PURPOSE: Create all database tables for Student Management System
# AUTHOR: Chandy Neat (updated by Trinh Dinh Nhat & ChatGPT)
# ==============================================================

import os
import sys
from mysql.connector import connect, Error

# ✅ Import config from root folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config


def create_tables():
    conn = None
    cursor = None

    try:
        print("🚀 Connecting to MySQL...")

        conn = connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )

        if conn.is_connected():
            cursor = conn.cursor()
            print("✅ Connected to MySQL successfully!")

            # ==================================================
            # 🧹 DROP OLD TABLES
            # ==================================================
            print("⚙️ Dropping existing tables (if any)...")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            cursor.execute("""
                DROP TABLE IF EXISTS 
                    audit_logs,
                    grades,
                    attendance,
                    subject_teacher,
                    subjects,
                    students,
                    classes,
                    teachers,
                    users;
            """)
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

            # ==================================================
            # 🧱 CREATE TABLES
            # ==================================================
            print("🧩 Creating tables...")

            # --- USERS ---
            cursor.execute("""
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
                email VARCHAR(150) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                role ENUM('admin', 'teacher') NOT NULL,
                image VARCHAR(255),
                status ENUM('active', 'inactive') DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # --- TEACHERS ---
            cursor.execute("""
            CREATE TABLE teachers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                name VARCHAR(150) NOT NULL,
                email VARCHAR(150) UNIQUE,
                contact VARCHAR(20),
                specialization VARCHAR(150),
                image VARCHAR(255),
                status ENUM('active', 'inactive') DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            );
            """)

            # --- CLASSES ---
            cursor.execute("""
            CREATE TABLE classes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                year INT NOT NULL,
                teacher_id INT,
                FOREIGN KEY (teacher_id) REFERENCES teachers(id)
                    ON UPDATE CASCADE
                    ON DELETE SET NULL
            );
            """)

            # --- STUDENTS ---
            cursor.execute("""
            CREATE TABLE students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(150) NOT NULL,
                gender ENUM('Male', 'Female', 'Other'),
                dob DATE,
                email VARCHAR(150) UNIQUE,
                contact VARCHAR(20),
                address TEXT,
                image VARCHAR(255),
                class_id INT,
                status ENUM('active', 'inactive') DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (class_id) REFERENCES classes(id)
                    ON UPDATE CASCADE
                    ON DELETE SET NULL
            );
            """)

            # --- SUBJECTS ---
            cursor.execute("""
            CREATE TABLE subjects (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(150) NOT NULL,
                image VARCHAR(255),
                class_id INT,
                FOREIGN KEY (class_id) REFERENCES classes(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            );
            """)

            # --- SUBJECT_TEACHER ---
            cursor.execute("""
            CREATE TABLE subject_teacher (
                id INT AUTO_INCREMENT PRIMARY KEY,
                subject_id INT NOT NULL,
                teacher_id INT NOT NULL,
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (subject_id) REFERENCES subjects(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
                FOREIGN KEY (teacher_id) REFERENCES teachers(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
                UNIQUE KEY unique_assignment (subject_id, teacher_id)
            );
            """)

            # --- ATTENDANCE ---
            cursor.execute("""
            CREATE TABLE attendance (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                class_id INT NOT NULL,
                date DATE NOT NULL,
                status ENUM('Present', 'Absent', 'Late', 'Excused') DEFAULT 'Present',
                FOREIGN KEY (student_id) REFERENCES students(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
                FOREIGN KEY (class_id) REFERENCES classes(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            );
            """)

            # --- GRADES ---
            cursor.execute("""
            CREATE TABLE grades (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                subject_id INT NOT NULL,
                class_id INT,
                teacher_id INT,
                term ENUM('Term 1', 'Term 2', 'Term 3', 'Final') DEFAULT 'Term 1',
                score DECIMAL(5,2) NOT NULL,
                grade_letter VARCHAR(2),
                remarks VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
                FOREIGN KEY (subject_id) REFERENCES subjects(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
                FOREIGN KEY (class_id) REFERENCES classes(id)
                    ON UPDATE CASCADE
                    ON DELETE SET NULL,
                FOREIGN KEY (teacher_id) REFERENCES teachers(id)
                    ON UPDATE CASCADE
                    ON DELETE SET NULL
            );
            """)

            # --- AUDIT LOGS ---
            cursor.execute("""
            CREATE TABLE audit_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                action TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
                    ON UPDATE CASCADE
                    ON DELETE SET NULL
            );
            """)

            # ==================================================
            # ✅ COMMIT CHANGES
            # ==================================================
            conn.commit()
            print("🎉 All tables created successfully with updated constraints!")

    except Error as e:
        print(f"❌ MySQL Error: {e}")

    except Exception as e:
        print(f"⚠️ Unexpected Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            print("🔒 MySQL connection closed.")


# ==============================================================
# MAIN EXECUTION
# ==============================================================
if __name__ == "__main__":
    create_tables()
