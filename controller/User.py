
from models.db import db
from models.User import User
from models.Permission import Group
from controller.Language import *
from controller.Permission import belongsToGroup, hasPermission, isCurrentUser, jwt_belongsToGroup
from controller.Request import createUser, login

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from flask_mail import Message
from App import app, api, mail, host
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask_jwt_extended import jwt_required, get_jwt_identity


# List Users
class UserList(Resource):
  @jwt_belongsToGroup("Admin")
  def get(self):
    response = []
    for user in User.query.all():
      response.append(user.email)
    return {'success': True, "users": response}



# User (post: Create, get: Show, put: Modify, delete: Delete)
class UserController(Resource):
  @jwt_required
  def get(self, id):
    user = User.query.filter_by(id = id).first()
    if user is None:
      return { 'success': False, 'message':UserDoesntExist }, 200
    elif not (isCurrentUser(user) or belongsToGroup('Admin')):
      return { 'success': False, 'message': InvalidToken }, 401
    return { 'success':  True, 
             'firstName':  user.firstName,
             'lastName':  user.lastName,
             'email':  user.email,
             'id': user.id,
             'active': False
          }, 201

  @jwt_required
  def put(self):
    return { success: True }, 200

  @jwt_belongsToGroup("Admin")
  def delete(self):
    return { success: True }, 200

  def post(self):
    json = createUser.parse_args()
    email = json["email"]
    id = json["id"]
    password = json["password"]


    userByEmail = User.query.filter_by(email = email).first()
    userById = User.query.filter_by(id = id).first()
    if userById is not None:
      return {'success':False, 'message': IDAlreadyExists}, 200
    if userByEmail is not None:
      return {'success':False, 'message': EmailAlreadyExists}, 200
      
    user = User( email = email,
                 firstName = json["firstName"],
                 lastName = json["lastName"],
                 id = json["id"],
                 active = False)
    user.hash_password(password)

    db.session.add(user)
    group = Group.query.filter_by(name = "Participant").first()
    if group == None:
      return {success: False, 'message':"Internal_Error: No default group found"}, 500
    group.users.append(user)
    db.session.commit()
    sendActivationEmail(user)
    return { 'success': True }, 201





# Activation of the user (An activation link is sent by email by the User controller's post method )
class UserActivate(Resource):
  def get(self, token):
    s = Serializer(app.config['JWT_SECRET_KEY'])
    try:
      data = s.loads(token)
      email = data["email"]
      id = data["id"]
      user = User.query.filter_by(id = id, email = email).first()
      if user is None:
        return app.make_response("<b>"+UserDoesntExist+"</b>")
      elif user.active:
        return app.make_response("<b>"+UserAlreadyActive+"</b>")
      user.activate()
      db.session.commit()

      return app.make_response("<b>"+UserActivated+"</b>")
    except SignatureExpired:
      return app.make_response("<b>"+ActivateTokenExpired+"</b>")
    except BadSignature:
      return app.make_response("<b>"+BadActivateToken+"</b>")

  def post(self):
    json = login.parse_args()
    email = json["email"]
    password = json["password"]

    user = User.query.filter_by(email = email).first()
    
    if user is None:
      return { "success": False, 'message': BadLoginCredentials }, 200
    elif not user.verify_password(password):
      return { "success": False, 'message': BadLoginCredentials }, 200
    elif user.active:
      return { "success": False, 'message': UserAlreadyActive }, 200
    else:
      sendActivationEmail(user)
      return { "success": True }, 200



# Authentication (Login)

class UserAuth(Resource):
  def post(self):
    json = login.parse_args()
    email = json["email"]
    password = json["password"]

    user = User.query.filter_by(email = email).first()
    
    if user is None or not user.verify_password(password):
      return { "success": False, 'code': 1, 'message': BadLoginCredentials }, 200
    elif not user.active:
      return { "success": False, 'code': 2, 'message': AccountNotActivated }, 200
    else: 
      token = user.generate_auth_token()

      permissions = {}
      for group in user.groups:
        for permission in group.permissions:
            permissions[permission.name] = True

      resp = { "success": True,
               "token": token,
               "firstName": user.firstName,
               "lastName": user.lastName,
               "id": user.id,
               "permissions": permissions }
      return resp, 201
      
# Router
api.add_resource(UserList, '/users')
api.add_resource(UserController, '/user/<string:id>', '/user')
api.add_resource(UserActivate, '/activate/user/<string:token>', '/activate/user')
api.add_resource(UserAuth, '/auth/user')


def sendActivationEmail(user):
  dump = { 'id': user.id, 'email': user.email, 'activation':True }
  token = Serializer(app.config['JWT_SECRET_KEY']).dumps(dump).decode('ascii')
  msg = Message(ActivateUserSubject, sender = 'smarticket.support', recipients = [user.email])
  msg.html = "<a href='"+host+"/activate/user/"+token+"'>Activar</a>"
  mail.send(msg)
