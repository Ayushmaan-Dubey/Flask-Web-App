#!/usr/bin/env python3
from website import create_app
from website import db
from website.models import User

app = create_app()
with app.app_context():
    email = input('Email to make admin: ').strip()
    user = User.query.filter_by(email=email).first()
    if not user:
        print('User not found')
    else:
        user.is_admin = True
        db.session.commit()
        print('User promoted to admin')
