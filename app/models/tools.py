from main import db
import datetime

class Tools(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(65536))
    vendor = db.Column(db.String(100))
    website_url = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    monthly_cost = db.Column(db.Float, nullable=False )
    active_users_count = db.Column(db.Integer, nullable=False, default=0 )
    owner_department = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), default='active')
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now(), nullable=False)

    def __repr__(self):
        return str(self.id)