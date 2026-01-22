from main import db
import datetime

class Usage_logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tool_id = db.Column(db.Integer, db.ForeignKey('tools.id'), nullable=False)
    session_date = db.Column(db.DateTime, nullable=False)
    usage_minutes = db.Column(db.Integer, default=0)
    actions_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)

    def __repr__(self):
        return str(self.id)