from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
import os

auth = Blueprint('auth', __name__)


@auth.route('/login', methods = ['Get', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Placeholder for authentication logic
        user = User.query.filter_by(email=email).first() 
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', 'success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', 'error')
        else:
            flash('Email does not exist.', 'error')
    data = request.form
    print(data)
    return render_template("login.html", user=current_user)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    errors = []
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        firstName = request.form.get('firstName', '').strip()
        password1 = request.form.get('password1', '')
        password2 = request.form.get('password2', '')

        if not email or not firstName or not password1 or not password2:
            errors.append('Please fill out all fields.')
        if password1 != password2:
            errors.append('Passwords do not match.')
        if len(password1) < 6:
            errors.append('Password must be at least 6 characters.')

        # check for existing email when using the database
        if db is not None:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                errors.append('An account with that email already exists.')

        if errors:
            return render_template('sign-up.html', errors=errors, form=request.form)

        # create user when db available; otherwise skip persistence
        if db is not None:
            new_user = User(email=email, first_name=firstName,
                            password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
        else:
            # no DB installed; skip storing user but still flash success for local testing
            pass

        flash('Account created successfully. You can now log in.', 'success')
        return redirect(url_for('views.home'))

    return render_template('sign-up.html', user =current_user)

# Admin-specific signup (creates an is_admin user) and login routes
@auth.route('/admin/signup', methods=['GET', 'POST'])
def admin_sign_up():
    # behave like regular signup but create an admin user
    errors = []
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        firstName = request.form.get('firstName', '').strip()
        password1 = request.form.get('password1', '')
        password2 = request.form.get('password2', '')
        pin = request.form.get('pin', '').strip()

        if not email or not firstName or not password1 or not password2:
            errors.append('Please fill out all fields.')
        if password1 != password2:
            errors.append('Passwords do not match.')
        if len(password1) < 6:
            errors.append('Password must be at least 6 characters.')

        # verify admin pin
        if pin != '2026':
            errors.append('Incorrect admin pin.')

        if db is not None:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                errors.append('An account with that email already exists.')

        if errors:
            return render_template('admin-sign-up.html', errors=errors, form=request.form)

        if db is not None:
            new_user = User(email=email, first_name=firstName,
                            password=generate_password_hash(password1, method='pbkdf2:sha256'),
                            is_admin=True)
            db.session.add(new_user)
            db.session.commit()
        else:
            # no DB; skip persistence for now
            pass

        flash('Admin account created successfully. You can now log in.', 'success')
        return redirect(url_for('views.home'))

    return render_template('admin-sign-up.html', errors=errors)


@auth.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    errors = []
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            errors.append('Please enter both email and password.')
            return render_template('admin-login.html', errors=errors)

        # local imports to avoid duplication
        from werkzeug.security import check_password_hash
        from flask_login import login_user

        if db is not None:
            user = User.query.filter_by(email=email).first()
            if not user or not getattr(user, 'is_admin', False):
                errors.append('Admin account not found.')
                return render_template('admin-login.html', errors=errors)

            if not check_password_hash(user.password, password):
                errors.append('Incorrect password.')
                return render_template('admin-login.html', errors=errors)

            login_user(user)
            flash('Logged in as admin.', 'success')
            return redirect(url_for('admin.admin_index'))
        else:
            errors.append('Database not available for login.')
            return render_template('admin-login.html', errors=errors)

    return render_template('admin-login.html')

@auth.route('/admin/logout')
def admin_logout():
    """Log out an admin and redirect to the admin login page."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.admin_login'))