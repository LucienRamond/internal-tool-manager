import os
from flask import Flask
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv(find_dotenv())

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")

db = SQLAlchemy(app)

from models import categories
from models import tools
from models import users
from models import user_tool_access
from models import usage_logs
from models import access_requests
from models import cost_tracking

with app.app_context():
    db.create_all()

if __name__ == "__name__":
        app.run(debug=True)
