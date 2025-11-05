# ===============================================================
# FILE: routes/auth.py
# DESCRIPTION: Authentication & User Management Routes
# ===============================================================
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.users_model import UserModel
from functools import wraps
from models.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# ---------------- Middleware: Require Login ----------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


# ---------------- Middleware: Require Admin ----------------
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'admin':
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated


# ---------------- Login ----------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("Please enter both email and password", "warning")
            return render_template('auth/login.html')

        user = UserModel.get_user_by_email(email)

        if user:
            # Admins can log in without password hashing
            if user['role'] == 'admin':
                # Direct login for admin (no password check)
                session['user_id'] = user['id']
                session['email'] = user['email']
                session['role'] = user['role']
                flash(f"Welcome back, Admin {user['email']}!", "success")
                return redirect(url_for('dashboard.dashboard_home'))

            # Normal user: verify hashed password
            elif check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['email'] = user['email']
                session['role'] = user['role']
                flash(f"Welcome back, {user['email']}!", "success")
                return redirect(url_for('dashboard.dashboard_home'))
            else:
                flash("Invalid email or password", "danger")
        else:
            flash("User not found", "danger")

    return render_template('auth/login.html')


# ---------------- Logout ----------------
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))


# ---------------- View Profile ----------------
@auth_bp.route('/profile')
@login_required
def view_profile():
    user = UserModel.get_user_by_id(session['user_id'])
    return render_template('users/profile.html', user=user)


# ---------------- Update Profile ----------------
@auth_bp.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    user_id = session['user_id']
    username = request.form.get('username')
    email = request.form.get('email')

    if not username or not email:
        flash("Username and Email cannot be empty.", "warning")
        return redirect(url_for('auth.view_profile'))

    UserModel.update_user(user_id, username=username, email=email)
    session['username'] = username

    flash("Profile updated successfully!", "success")
    return redirect(url_for('auth.view_profile'))


# ---------------- Change Password ----------------
@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current = request.form.get('current_password')
        new = request.form.get('new_password')
        confirm = request.form.get('confirm_password')

        user = UserModel.get_user_by_id(session['user_id'])

        if not check_password_hash(user['password_hash'], current):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for('auth.change_password'))

        if new != confirm:
            flash("New passwords do not match.", "warning")
            return redirect(url_for('auth.change_password'))

        UserModel.change_password(session['user_id'], new)
        flash("Password changed successfully!", "success")
        return redirect(url_for('auth.view_profile'))

    return render_template('users/change_password.html')


@auth_bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        role = request.form.get('role')
        if role not in ["teacher", "student", "admin"]:
            flash("⚠️ Invalid role selected.", "warning")
            return redirect(url_for('auth.create_user'))
        print(role)
        # Check if username or email already exists
        if UserModel.get_user_by_username(username):
            flash("⚠️ Username already exists.", "warning")
        elif UserModel.get_user_by_email(email):
            flash("⚠️ Email already exists.", "warning")
        else:
            password_hash = generate_password_hash(password)
            UserModel.create_user(
                username=username,
                email=email,
                password_hash=password_hash,
                role=role
            )
            flash("✅ User created successfully!", "success")
            return redirect(url_for('auth.manage_users'))

    return render_template('users/create_user.html')


# ---------------- Update User (Admin) ----------------
@auth_bp.route('/update/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def update_user(user_id):
    user = UserModel.get_user_by_id(user_id)

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        role = request.form.get('role')
        password = request.form.get('password')

        pass_hash = generate_password_hash(password) if password else None

        UserModel.update_user(user_id, username=username, email=email, role=role, password_hash=pass_hash)

        flash("User updated successfully!", "success")
        return redirect(url_for('auth.manage_users'))

    return render_template('users/update_user.html', user=user)


# ---------------- Delete User (Admin) ----------------
@auth_bp.route('/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    UserModel.delete_user(user_id)
    flash("User deleted successfully!", "info")
    return redirect(url_for('auth.manage_users'))


# ---------------- Manage Users (Admin) ----------------
@auth_bp.route('/manage')
@login_required
@admin_required
def manage_users():
    users = UserModel.get_all_users(exclude_admin=False)
    return render_template('users/manage_users.html', users=users)
