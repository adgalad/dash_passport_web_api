from App import admin
from models.db import db

from flask_admin.contrib.sqla import ModelView

class Purchase(db.Model):
	__tablename__ = "db_purchase"
	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	donation = db.Column(db.Boolean, default=False, nullable=False)
	rrss = db.Column(db.Boolean, default=False, nullable=False)
	passport_id = db.Column(db.Integer, db.ForeignKey('db_passport.id'))

class Vendor(db.Model):
	__tablename__ = "db_vendor"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(42), nullable=False)

# La clave primaria de esta clase es compuesta
class BuysToVendor(db.Model):
	__tablename__ = "db_buysToVendor"
	purchase_id = db.Column(db.Integer, db.ForeignKey('db_purchase.id'), primary_key=True)
	vendor_id = db.Column(db.Integer, db.ForeignKey('db_vendor.id'), primary_key=True)
	stamps = db.Column(db.Float, default=0.0, nullable=False)
	prize = db.Column(db.Float, default=0.0, nullable=False)

# La clave primaria de esta clase es compuesta
class ParticipatesIn(db.Model):
	__tablename__ = "db_participatesIn"
	vendor_id = db.Column(db.Integer, db.ForeignKey('db_vendor.id', primary_key=True))
	event_id = db.Column(db.Integer, db.ForeignKey('db_event.id'), primary_key=True)

admin.add_view(ModelView(Purchase, db.session))
admin.add_view(ModelView(Vendor, db.session))
admin.add_view(ModelView(BuysToVendor, db.session))
admin.add_view(ModelView(ParticipatesIn, db.session))