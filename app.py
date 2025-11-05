# ==============================================================
# FILE: app.py
# PURPOSE: Main Flask application entry point
# AUTHOR: Chandy Neat
# ==============================================================

from flask import Flask, render_template, redirect, url_for
from datetime import datetime
from config import Config

# ==============================================================
# 🔹 Initialize Flask App
# ==============================================================
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']

# ==============================================================
# 🔹 Import & Register Blueprints
# ==============================================================
from routes.auth import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.subjects_routes import subjects_bp
from routes.student_routes import student_bp
from routes.attendance_routes import attendance_routes
from routes.teacher_routes import teacher_routes
from routes.grade_routes import grade_bp   # ✅ Added Grade Routes
from routes.class_routes import classes_bp  # ✅ Added Grade Routes

# Register all blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(subjects_bp)
app.register_blueprint(student_bp)
app.register_blueprint(attendance_routes)
app.register_blueprint(teacher_routes)
app.register_blueprint(grade_bp)  # ✅ Register new grade blueprint
app.register_blueprint(classes_bp)  # ✅ Register new grade blueprint

# ==============================================================
# 🔹 Global Template Variables
# ==============================================================
@app.context_processor
def inject_globals():
    """Inject current year globally into templates."""
    return {'current_year': datetime.now().year}

# ==============================================================
# 🔹 Routes
# ==============================================================
@app.route('/')
def home():
    """Redirect to login page."""
    return redirect(url_for('auth.login'))

# ==============================================================
# 🔹 Error Handlers
# ==============================================================
@app.errorhandler(404)
def not_found(e):
    """Custom 404 page."""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Custom 500 page."""
    return render_template('errors/500.html'), 500

# ==============================================================
# 🔹 Run Application
# ==============================================================
if __name__ == '__main__':
    app.run(debug=True)
