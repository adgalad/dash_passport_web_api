
from models.User import User
from models.Permission import Group, Permission
from controller.Language import *

from flask_jwt_extended import get_jwt_identity, jwt_required

@jwt_required
def belongsToGroup(groupName):
  currentUser = get_jwt_identity()
  groups = Group.query.filter_by(name = groupName)
  for group in groups:
    for member in group.users:
      if member.id == currentUser["id"]:
        return True
  return False
@jwt_required
def hasPermission(permissionName):
  currentUser = get_jwt_identity()
  users = User.query.filter_by(id = currentUser['id'])
  for user in users:
    for group in user.groups:
      for permission in group.permissions:
        if permission.name == permissionName:
          return True
  return False
@jwt_required
def isCurrentUser(user):
  currentUser = get_jwt_identity()
  print(currentUser)
  return user.id == currentUser["id"]


def jwt_hasPermission(permissionName):
  def wrap(f):
    @jwt_required
    def wrapped_f(*args):
      if hasPermission(permissionName):      
        return f(*args)
      else:
        return {'success': False, 'message':UnauthorizedAccess}, 401
    return wrapped_f
  return wrap

def jwt_belongsToGroup(groupName):
  def wrap(f):
    @jwt_required
    def wrapped_f(*args):
      if belongsToGroup(groupName):      
        return f(*args)
      else:
        return {'success': False, 'message':UnauthorizedAccess}, 401
    return wrapped_f
  return wrap