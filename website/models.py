from . import db
from sqlalchemy import func
from flask_login import UserMixin

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(1000))
    remind_at = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

if db is not None:
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(150), unique=True)
        password = db.Column(db.String(150))
        first_name = db.Column(db.String(150) )
        notes = db.relationship('Note')

        def __repr__(self):
            return f"<User {self.email}>"
else:
    class User(UserMixin):
        def __init__(self, email, first_name, password):
            self.email = email
            self.first_name = first_name
            self.password = password

        def __repr__(self):
            return f"<User {self.email}>"