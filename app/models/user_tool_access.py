from main import db
import datetime

class User_tool_access(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tool_id = db.Column(db.Integer, db.ForeignKey('tools.id'), nullable=False)
    granted_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    granted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    revoked_at = db.Column(db.DateTime)
    revoked_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(255), default='active')

    def __repr__(self):
        return str(self.id)