from models.db import db
from App import admin

from flask_admin.contrib.sqla import ModelView


# This is the association table for the many-to-many relationship between
# groups and permissions.
group_permission_table = db.Table('db_group_permission', db.Model.metadata,
  db.Column('group_id', db.Integer, db.ForeignKey('db_group.id',onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
  db.Column('permission_id', db.Integer, db.ForeignKey('db_permission.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True))


# This is the association table for the many-to-many relationship between
# groups and members - this is, the memberships.
user_group_table = db.Table('db_user_group', db.Model.metadata,
  db.Column('user_id', db.Integer, db.ForeignKey('db_user.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
  db.Column('group_id', db.Integer, db.ForeignKey('db_group.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True))



class Group(db.Model):
  __tablename__ = 'db_group'
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  name = db.Column(db.String(32), unique=True, nullable=False)
  users = db.relation('User', secondary=user_group_table, backref='groups')
  
  def __repr__(self):
    return '%r' % self.name

class Permission(db.Model):
  __tablename__ = 'db_permission'
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  name = db.Column(db.String(32), unique=True, nullable=False)
  # description = Column(Unicode(255))
  groups = db.relation(Group, secondary=group_permission_table, backref='permissions')
  
  def __repr__(self):
    return '%r' % self.name


admin.add_view(ModelView(Group, db.session))
admin.add_view(ModelView(Permission, db.session))