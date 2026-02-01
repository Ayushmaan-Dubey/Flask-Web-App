from flask import Blueprint, render_template, send_from_directory, current_app
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("Home.HTML", user = current_user)


@views.route('/manifest.json')
def manifest():
    return send_from_directory(current_app.static_folder, 'manifest.json')


@views.route('/sw.js')
def service_worker():
    response = send_from_directory(current_app.static_folder, 'sw.js')
    response.headers['Cache-Control'] = 'no-cache'
    return response


@views.route('/offline')
def offline():
    return render_template('offline.html')