from main import db
import datetime

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    department = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(150), default='employee')
    status = db.Column(db.String(150), default='active')
    hire_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now(), nullable=False)

    def __repr__(self):
        return str(self.id)