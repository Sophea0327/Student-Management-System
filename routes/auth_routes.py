# ===============================================================
# FILE: routes/auth.py
# DESCRIPTION: Authentication & User Management Routes
# ===============================================================
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.users_model import UserModel
from functools import wraps
from models.db import get_db
from werkzeug.security import check_password_hash

# Blueprint setup
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# ---------------- Middleware: Require login ----------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


# ---------------- Middleware: Require admin ----------------
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'admin':
            flash("You do not have permission to access this page.", "danger")
            # ✅ Fix redirect endpoint
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated


# ---------------- Login ----------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login with hashing for users, plain text for admin"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Please enter both username and password", "warning")
            return render_template('auth/login.html')

        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # ✅ Check login by role
            if user['role'] == 'admin':
                # Admin uses plain-text password
                if user['password_hash'] == password:
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['role'] = user['role']
                    flash(f"Welcome Admin, {user['username']}!", "success")
                    return redirect(url_for('dashboard.index'))
                else:
                    flash("Invalid admin password", "danger")

            else:
                # Teachers/Students use hashed passwords
                if check_password_hash(user['password_hash'], password):
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['role'] = user['role']
                    flash(f"Welcome back, {user['username']}!", "success")
                    return redirect(url_for('dashboard.index'))
                else:
                    flash("Invalid username or password", "danger")

        else:
            flash("User not found", "danger")

    return render_template('auth/login.html')

# ---------------- Logout ----------------
@auth_bp.route('/logout')
def logout():
    """Logs the user out"""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))


# ---------------- View Profile ----------------
@auth_bp.route('/profile')
@login_required
def view_profile():
    """Display current user profile"""
    user = UserModel.get_user_by_id(session['user_id'])
    return render_template('users/profile.html', user=user)


# ---------------- Update Own Profile ----------------
@auth_bp.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    """Allow the logged-in user to update their username and email"""
    user_id = session['user_id']
    username = request.form.get('username')
    email = request.form.get('email')

    if not username or not email:
        flash("⚠️ Username and Email cannot be empty.", "warning")
        return redirect(url_for('auth.view_profile'))

    UserModel.update_user(user_id, username=username, email=email)
    session['username'] = username  # Update session for display
    flash("✅ Profile updated successfully!", "success")
    return redirect(url_for('auth.view_profile'))


# ---------------- Update Profile Image ----------------
@auth_bp.route('/update_profile_image', methods=['POST'])
@login_required
def update_profile_image():
    """Update the logged-in user's profile picture"""
    user_id = session['user_id']
    file = request.files.get('profile_image')

    if not file:
        flash("⚠️ No file selected.", "warning")
        return redirect(url_for('auth.view_profile'))

    # Save the file
    import os
    from werkzeug.utils import secure_filename

    filename = secure_filename(file.filename)
    upload_path = os.path.join('static', 'uploads', filename)
    file.save(upload_path)

    # Update database
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE users SET profile_image = %s WHERE id = %s", (f'/static/uploads/{filename}', user_id))
    db.commit()
    cursor.close()

    flash("✅ Profile image updated successfully!", "success")
    return redirect(url_for('auth.view_profile'))


# ---------------- Change Password ----------------
@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Allow user to change their password"""
    if request.method == 'POST':
        current = request.form.get('current_password')
        new = request.form.get('new_password')
        confirm = request.form.get('confirm_password')

        user = UserModel.get_user_by_id(session['user_id'])

        if not UserModel.verify_password(user['password_hash'], current):
            flash("⚠️ Current password is incorrect.", "danger")
            return redirect(url_for('auth.change_password'))

        if new != confirm:
            flash("⚠️ New passwords do not match.", "warning")
            return redirect(url_for('auth.change_password'))

        UserModel.change_password(session['user_id'], new)
        flash("✅ Password changed successfully!", "success")
        return redirect(url_for('auth.view_profile'))

    return render_template('users/change_password.html')

# ---------------- Update User ----------------
@auth_bp.route('/update/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def update_user(user_id):
    """Admin can update user info"""
    user = UserModel.get_user_by_id(user_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('auth.manage_users'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        role = request.form.get('role')
        password = request.form.get('password')

        # Update user info
        UserModel.update_user(
            user_id,
            username=username,
            email=email,
            role=role,
            password=password if password else None
        )

        flash("✅ User updated successfully!", "success")
        return redirect(url_for('auth.manage_users'))

    return render_template('users/update_user.html', user=user)


# ---------------- Create User (Admin Only) ----------------
@auth_bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    """Admin can create a new user"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'teacher')

        existing_user = UserModel.get_user_by_username(username)
        if existing_user:
            flash("⚠️ Username already exists. Choose another.", "warning")
        else:
            UserModel.create_user(username=username, email=email, password=password, role=role)
            flash("✅ User created successfully!", "success")
            return redirect(url_for('auth.manage_users'))

    return render_template('users/create_user.html')


# ---------------- Delete User (Admin Only) ----------------
@auth_bp.route('/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Admin can delete a user"""
    user = UserModel.get_user_by_id(user_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('auth.manage_users'))

    UserModel.delete_user(user_id)
    flash("🗑️ User deleted successfully!", "info")
    return redirect(url_for('auth.manage_users'))


# ---------------- Manage Users (Admin Only) ----------------
@auth_bp.route('/manage')
@login_required
@admin_required
def manage_users():
    """Admin view to manage all users"""
    users = UserModel.get_all_users(exclude_admin=False)
    return render_template('users/manage_users.html', users=users)
