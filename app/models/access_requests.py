from main import db
import datetime

class Access_requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tool_id = db.Column(db.Integer, db.ForeignKey('tools.id'), nullable=False)
    business_justification = db.Column(db.String(65536), nullable=False)
    status = db.Column(db.String(255), default='pending')
    requested_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    processed_at = db.Column(db.DateTime)
    processed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    processing_notes = db.Column(db.String(65536))

    def __repr__(self):
        return str(self.id)