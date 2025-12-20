from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

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