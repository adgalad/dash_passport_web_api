
from models.db import db
from models.User import User
from models.Passport import Passport
from models.Event import Event
from models.Vendor import Vendor
from controller.Language import *
from controller.Permission import belongsToGroup, hasPermission, isCurrentUser, jwt_belongsToGroup
from controller.Request import createEvent, desactivateEvent

from flask_restful import Resource
from App import app, api
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime
import time




# List Users
class EventList(Resource):
  @jwt_belongsToGroup("Admin")
  def get(self):
    response = []
    for event in Event.query.all():
      response.append(str(event))
    return {'success': True, "events": response}



# User (post: Create, get: Show, put: Modify, delete: Delete)
class EventController(Resource):

  def get(self, id):
    event = Event.query.filter_by(id = id).first()


    return { 'date': time.mktime(event.date.timetuple()),
             'active': event.active,
             'name': event.name,
             'location': event.location,
             'duff_value': event.duff_value,
             'id': event.id }


  @jwt_belongsToGroup("Admin")
  def put(self):
    json = desactivateEvent.parse_args()
    event = Event.query.filter_by(id = json["id"]).first()
    event.active = False
    for passport in event.passports:
      passport.activated = False
      passport.recharged = True
    db.session.commit()
    return { 'success': True }, 200

  def post(self):
    json = createEvent.parse_args()
    date = datetime.datetime.fromtimestamp(int(json["date"]))
    createEvent(date=date,
               name=json["name"],
               location=json["location"],
               duff_value=json["duff_value"])
    
    return { 'success': True }, 200

class EventVendors(Resource):
  def get(self, id):
    event = Event.query.filter_by(id = id).first()
    
    query = Vendor.query.filter_by(event_id = event.id, isFoundation=False)
    vendors = {}
    for i in query:
      vendors[str(i.name)] = i.id
    return {'success': True, 'vendors': vendors}, 201

class EventFoundations(Resource):
  def get(self, id):
    event = Event.query.filter_by(id = id).first()
    
    query = Vendor.query.filter_by(event_id = event.id, isFoundation=True)
    vendors = {}
    for i in query:
      vendors[str(i.name)] = i.id
    return {'success': True, 'vendors': vendors}, 201

    


# Router
api.add_resource(EventList, '/events')
api.add_resource(EventController, '/event/<string:id>', '/event')
api.add_resource(EventVendors, '/event/<string:id>/vendors')
api.add_resource(EventFoundations, '/event/<string:id>/foundations')

def createEvent(date, name, location, duff_value, active=True):
  event = Event( date=date, name=name, location=location,
                 duff_value=duff_value, active=active)
  db.session.add(event)
  dummy_passport = Passport(user_id=1, event=event) 
  db.session.add(dummy_passport)
  db.session.commit()
  event.dummy_passport = dummy_passport.id
  db.session.commit()