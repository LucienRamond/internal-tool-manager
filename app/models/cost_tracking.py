from main import db
import datetime

class Cost_tracking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tool_id = db.Column(db.Integer, db.ForeignKey('tools.id'), nullable=False)
    month_year = db.Column(db.DateTime, nullable=False)
    total_monthly_cost = db.Column(db.Float, nullable=False )
    active_users_count = db.Column(db.Integer, nullable=False, default=0 )
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)

    def __repr__(self):
        return str(self.id)