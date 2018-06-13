from App import admin
from models.db import db

from flask_admin.contrib.sqla import ModelView

vendor_event_table = db.Table('db_vendor_event', db.Model.metadata,
    db.Column('vendor_id', db.Integer, db.ForeignKey('db_vendor.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('db_event.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
)


class Event(db.Model):
  __tablename__ = "db_event"
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  date = db.Column(db.Date, nullable=False)
  location = db.Column(db.String, nullable=False)
  duff_value = db.Column(db.Float, nullable=False)
  name = db.Column(db.String, nullable=False)
  active = db.Column(db.Boolean, default=True, nullable=False)
  vendors = db.relationship('Vendor', secondary=vendor_event_table, back_populates="events") 
  dummy_passport = db.Column(db.Integer, nullable = True)
  
  def __repr__(self):
    return '<Event %r>' % self.name
