from App import admin
from models.db import db
from models.Event import Event
from models.User import User

from flask_admin.contrib.sqla import ModelView

class Passport(db.Model):
  __tablename__ = "db_passport"
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  stamps = db.Column(db.Float, default=0.0, nullable=False)
  donations = db.Column(db.Float, default=0.0, nullable=False)
  activated = db.Column(db.Boolean, default=False, nullable=False)
  recharged = db.Column(db.Boolean, default=False, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('db_user.id'))
  event_id = db.Column(db.Integer, db.ForeignKey('db_event.id'))
  user = db.relation(User, backref='passport')  
  event = db.relation(Event, backref='passport')  

admin.add_view(ModelView(Passport, db.session))