
from models.db import db
from models.User import User
from models.Passport import Passport
from controller.Language import *
from controller.Permission import belongsToGroup, hasPermission, isCurrentUser, jwt_belongsToGroup
from controller.Request import createPassport

from flask_restful import Resource
from App import app, api
from flask_jwt_extended import jwt_required, get_jwt_identity






# List Users
class PassportList(Resource):
  @jwt_belongsToGroup("Admin")
  def get(self):
    response = []
    for passport in PassportList.query.all():
      response.append(str(passport))
    return {'success': True, "passports": response}



# User (post: Create, get: Show, put: Modify, delete: Delete)
class PassportController(Resource):
  @jwt_required
  def get(self, id):
    passport = Passport()
    

  @jwt_required
  def put(self):
    
    return { success: True }, 200

  @jwt_belongsToGroup("Admin")
  def delete(self):
    return { success: True }, 200

  def post(self):
    json = createUser.parse_args()
    user_id = json["user_id"]
    passport = Passport(user_id = user_id)
    db.session.add(passport)
    db.session.commit()
    return { 'success': True }, 201




# Router
api.add_resource(PassportList, '/passports')
api.add_resource(PassportController, '/passport/<string:id>', '/passport')
api.add_resource(PassportActivate, '/activate/passport/<string:token>')


