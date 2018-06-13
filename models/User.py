from App import app, jwt, admin
from models.db import db
from passlib.apps import custom_app_context as pwd_context
from flask_jwt_extended import create_access_token
from flask_admin.contrib.sqla import ModelView





class User(db.Model):
  __tablename__ = 'db_user'
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  email = db.Column(db.String(128), unique=True, nullable=False)
  firstName = db.Column(db.String(32), nullable=False)
  lastName = db.Column(db.String(32), nullable=False)
  active = db.Column(db.Boolean, nullable=False)
  password_hash = db.Column(db.String(128), nullable=False)

  def __repr__(self):
    return '<User %r>' % self.email

  def hash_password(self, password):
    self.password_hash = pwd_context.encrypt(password)

  def activate(self):
    self.active = True

  def verify_password(self, password):
    return pwd_context.verify(password, self.password_hash)

  #Generate a token using flask_jwt_extended
  def generate_auth_token(self, expiration = 600):
    identity = { 'id': self.id, 'email': self.email }
    return create_access_token(identity = identity, expires_delta=False)



