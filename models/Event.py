from App import admin
from models.db import db

from flask_admin.contrib.sqla import ModelView

class Event(db.Model):
  __tablename__ = "db_event"
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  date = db.Column(db.Date, nullable=False)
  location = db.Column(db.String, nullable=False)
  duff_value = db.Column(db.Float, nullable=False)

admin.add_view(ModelView(Event, db.session))