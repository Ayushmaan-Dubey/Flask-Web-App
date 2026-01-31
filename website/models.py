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
        email = db.Column(db.String(150), unique=True, nullable=False)
        password = db.Column(db.String(150), nullable=False)
        first_name = db.Column(db.String(150), nullable=False)
        last_name = db.Column(db.String(150), nullable=True)
        notes = db.relationship('Note')
        is_admin = db.Column(db.Boolean, default=False, nullable=False)
        first_time_at_temple = db.Column(db.Boolean, default=False, nullable=False)
        contact_date = db.Column(db.Date, nullable=True)
        area = db.Column(db.String(200), nullable=True)
        interests = db.Column(db.String(500), nullable=True)  # comma-separated
        event_source = db.Column(db.String(200), nullable=True)
        created_by_admin = db.Column(db.String(200), nullable=True)  # new field

        def __repr__(self):
            return f"<User {self.email}>"
else:
    class User(UserMixin):
        def __init__(self, email, first_name, password, is_admin=False, last_name=None,
                     first_time_at_temple=False, contact_date=None, area=None, interests=None, event_source=None, created_by_admin=None):
            self.email = email
            self.first_name = first_name
            self.last_name = last_name
            self.password = password
            self.is_admin = is_admin
            self.first_time_at_temple = first_time_at_temple
            self.contact_date = contact_date
            self.area = area
            self.interests = interests
            self.event_source = event_source
            self.created_by_admin = created_by_admin  # new field

        def __repr__(self):
            return f"<User {self.email}>"