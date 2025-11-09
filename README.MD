# 🎓 Student Management System

A Flask-based web application designed to manage students, teachers, classes, attendance, grades, and subjects efficiently.  
This system provides separate roles for **Admin**, **Teacher**, and **Student**, making it easy to manage and monitor academic activities.

---

## 🚀 Features

- 👩‍💼 **Admin Panel**
  - Manage teachers, students, classes, subjects, and grades.
  - Assign subjects or classes to teachers.
  - View dashboard with total counts and activity summary.

- 👨‍🏫 **Teacher Module**
  - Manage attendance and grades for assigned classes.
  - View class and student lists.

- 👩‍🎓 **Student Module**
  - View personal grades, attendance records, and class information.

- 🔒 **Authentication System**
  - Login and role-based access control (Admin / Teacher / Student).

---

## 🏗️ Project Structure

```plaintext
STUDENT-MANAGEMENT-SYSTEM/
│
├── models/                     # Database models (handle CRUD operations)
│   ├── student_model.py
│   ├── teacher_model.py
│   ├── class_model.py
│   ├── subject_model.py
│   ├── attendance_model.py
│   ├── grade_model.py
│   ├── dashboard_model.py
│   └── users_model.py
│
├── routes/                     # Application routes (Controllers)
│   ├── auth.py
│   ├── student_routes.py
│   ├── teacher_routes.py
│   ├── class_routes.py
│   ├── subjects_routes.py
│   ├── attendance_routes.py
│   ├── grade_routes.py
│   └── dashboard_routes.py
│
├── templates/                  # HTML templates (Views)
│   ├── auth/
│   ├── students/
│   ├── teachers/
│   ├── classes/
│   ├── subjects/
│   ├── attendance/
│   ├── grade/
│   ├── dashboard/
│   ├── users/
│   ├── errors/
│   ├── layout.html
│   └── dashboard_admin.html
│
├── static/                     # Static assets (CSS, JS, Images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── seeders/
│   └── seed_data.py            # Insert sample data into database
│
├── utils/                      # Helper or common functions (if any)
│
├── app.py                      # Main Flask app (entry point)
├── config.py                   # App configuration and database setup
├── migrate.py                  # Create or migrate database tables
├── requirements.txt            # List of required Python packages
├── .env                        # Environment variables (DB credentials)
└── README.md                   # Project documentation

```
---


---

## ⚙️ Installation

### 1️⃣ Clone or Copy the Project
```bash
git clone https://github.com/your-username/student-management-system.git
cd student-management-system
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
```
### 3️⃣ Activate the Virtual Environment
#### On Window:
```bash
venv\Scripts\activate
```
#### On MacOS/Linux:
```bash
source venv/bin/activate
```
### 4️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 5️⃣ Configure Database
Create a MySQL database and update your .env or config.py:
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DB=student_management
SECRET_KEY=your_secret_key
```
### 6️⃣ Run Database Migration
```bach
python migrate.py
```
### 7️⃣ (Optional) Seed Sample Data
```bash
python seeders/seed_data.py
```
### 8️⃣ Run the application
```bash
python app.py
```
### The app should run on:
```cpp
http://127.0.0.1:5000/
```

## 👩‍💻 Features

- **🔐 User Authentication (Admin, Teacher, Student)**
- **🧑‍🎓 Manage Students (Add / Edit / Delete / View)**
- **👩‍🏫 Manage Teachers**
- **🏫 Manage Classes and Subjects**
- **🕐 Record and View Attendance**
- **📝 Manage Student Grades**
- **📊 Dashboard Summary (students, teachers, classes, etc.)**
- **⚙️ Role-Based Access Control**

## 🧠 Developer Documentation
### 📄 See the file:
```bash
/documents/developer_documentation.docx
```
for explanation of all modules, functions, and their purpose.

## 🧪 Test Document
### 📄 See the file:
```bash
/documents/test_document.docx
```
for full test cases (login, add student, attendance, grades, etc.).

## 🧰 Tools & Technologies
- **Backend: Python (Flask)**
- **Frontend: HTML, CSS, Bootstrap**
- **Database: MySQL**
- **Environment: Virtual Environment (venv)**
- **Testing Tools: Manual testing, Postman**

## 👨‍💻 Author
**Name:**  Sophorn Sophea

**ID:**  063

**Major:** Web-Developer

**Project:** Student Management System 

```yaml

---

### 💡 How to Add It in VS Code
1. Open your project in VS Code.  
2. Right-click on the root folder (`STUDENT-MANAGEMENT-SYSTEM`).  
3. Click **New File** → name it **`README.md`**.  
4. Paste the code above.  
5. Save it (Ctrl + S).  
6. You’ll see Markdown formatting automatically highlighted.

---

Would you like me to **add Khmer translations** (for example, small Khmer explanation below each section like “អំពីប្រព័ន្ធ”, “តម្រូវការដំឡើង”, “ការប្រើប្រាស់”) so it looks bilingual for your teacher’s report?
```