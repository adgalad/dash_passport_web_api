import sys
sys.path.insert(0, '../')
from App import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)


