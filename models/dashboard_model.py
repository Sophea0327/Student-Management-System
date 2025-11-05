import mysql.connector
from mysql.connector import Error
from datetime import datetime


class DashboardModel:
    def __init__(self, db_config):
        """
        db_config: dictionary with host, user, password, and database keys.
        Example:
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "student_performance"
        }
        """
        self.db_config = db_config

    def _get_connection(self):
        return mysql.connector.connect(**self.db_config)

    # ------------------ TEACHER DASHBOARD ------------------

    def get_teacher_dashboard_data(self):
        """Get total students, subjects, average per class, and overall average."""
        connection = self._get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            # Total subjects
            cursor.execute("SELECT COUNT(*) AS total_subjects FROM subjects;")
            total_subjects = cursor.fetchone()["total_subjects"]

            # Total students
            cursor.execute("SELECT COUNT(*) AS total_students FROM students;")
            total_students = cursor.fetchone()["total_students"]

            # Average scores by class
            cursor.execute("""
                SELECT c.class_name, AVG(s.score) AS avg_score
                FROM student_scores s
                JOIN classes c ON s.class_id = c.id
                GROUP BY c.id;
            """)
            avg_data = cursor.fetchall()

            class_names = [row["class_name"] for row in avg_data]
            avg_scores = [float(row["avg_score"]) for row in avg_data]

            # Overall average
            cursor.execute("SELECT AVG(score) AS overall_avg FROM student_scores;")
            overall_avg = round(cursor.fetchone()["overall_avg"] or 0, 2)

            return {
                "total_subjects": total_subjects,
                "total_students": total_students,
                "class_names": class_names,
                "avg_scores": avg_scores,
                "overall_avg": overall_avg
            }

        except Error as e:
            print(f"Error fetching teacher dashboard data: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

    # ------------------ STUDENT DASHBOARD ------------------

    def get_student_dashboard_data(self, student_id):
        """Get performance summary for a specific student."""
        connection = self._get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            # Scores by subject
            cursor.execute("""
                SELECT sub.subject_name, s.score
                FROM student_scores s
                JOIN subjects sub ON s.subject_id = sub.id
                WHERE s.student_id = %s;
            """, (student_id,))
            score_data = cursor.fetchall()

            subjects = [row["subject_name"] for row in score_data]
            scores = [float(row["score"]) for row in score_data]

            # GPA (example: assuming 100-point scale -> 4.0 scale)
            cursor.execute("""
                SELECT AVG(score) AS avg_score FROM student_scores WHERE student_id = %s;
            """, (student_id,))
            avg_score = cursor.fetchone()["avg_score"] or 0
            gpa = round((avg_score / 25), 2)  # 100 -> 4.0 scale conversion

            # Rank among classmates (based on average score)
            cursor.execute("""
                SELECT student_id, AVG(score) AS avg_score
                FROM student_scores
                GROUP BY student_id
                ORDER BY avg_score DESC;
            """)
            all_students = cursor.fetchall()

            rank = next(
                (i + 1 for i, row in enumerate(all_students) if row["student_id"] == student_id),
                None
            )

            return {
                "subjects": subjects,
                "scores": scores,
                "gpa": gpa,
                "rank": rank
            }

        except Error as e:
            print(f"Error fetching student dashboard data: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
