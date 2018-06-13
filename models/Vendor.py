from App import admin
from models.db import db
from models.Passport import Passport
from models.Event import Event, vendor_event_table
from models.User import User

from flask_admin.contrib.sqla import ModelView

import datetime

product_purchase_table = db.Table('db_product_purchase', db.Model.metadata,
    db.Column('product_id', db.Integer, db.ForeignKey('db_product.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    db.Column('purchase_id', db.Integer, db.ForeignKey('db_purchase.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
  	db.Column('amount', db.Integer, default=1, nullable=False)  
)

class Vendor(db.Model):
	__tablename__ = "db_vendor"
	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('db_user.id'), nullable=False)
	user = db.relation(User, backref='vendor')
	name = db.Column(db.String(42), nullable=False)
	isFoundation = db.Column(db.Boolean, default=False, nullable=False)
	events = db.relationship(Event, secondary=vendor_event_table)
	def __repr__(self):
		return self.name

class Product(db.Model):
	__tablename__ = "db_product"
	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	vendor_id = db.Column(db.Integer, db.ForeignKey('db_vendor.id'))
	name = db.Column(db.String(42), nullable=False)
	price = db.Column(db.Float, nullable=False)
	vendor = db.relation(Vendor, backref='products')
	purchases = db.relationship('Purchase', secondary=product_purchase_table, back_populates="products")

	def __repr__(self):
		return self.name

class Purchase(db.Model):
	__tablename__ = "db_purchase"
	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	donation = db.Column(db.Boolean, default=False, nullable=False)
	passport_id = db.Column(db.Integer, db.ForeignKey('db_passport.id'), nullable=False)
	passport = db.relation(Passport, backref='purchases')
	id_client = db.Column(db.Integer, nullable=True)
	price = db.Column(db.Float, nullable=False)
	datetime = db.Column(db.DateTime, default=datetime.datetime.now())
	products = db.relationship('Product', secondary=product_purchase_table)	
	vendor_id = db.Column(db.Integer, db.ForeignKey('db_vendor.id'), nullable=False)
	vendor = db.relation(Vendor, backref='purchases')

	def __repr__(self):
		return str(self.products)

# La clave primaria de esta clase es compuesta



#participateIn