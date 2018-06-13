
from models.db import db
from models.User import User
from models.Passport import Passport
from models.Vendor import *
from controller.Language import *
from controller.Permission import belongsToGroup, hasPermission, isCurrentUser, jwt_belongsToGroup, jwt_hasPermission
from controller.Request import createPassport, passportOperation, passportStamp

from flask_restful import Resource
from App import app, api
from flask_jwt_extended import jwt_required, get_jwt_identity






class PassportList(Resource):
  @jwt_belongsToGroup("Admin")
  def get(self):
    response = []
    for passport in Passport.query.all():
      response.append(str(passport))
    return {'success': True, "passports": response}



class PassportController(Resource):
  @jwt_required
  def get(self, id):
    passport = Passport.query.filter_by(id = id).first()
    if passport is None:
      return { 'success': False, 'message': PassportNotFound(id)}
    donations = 0 if passport.donations == 0 else passport.donations + 1
    rechargeValue = passport.event.duff_value * (passport.stamps + donations)
    return { 'success': True,
             'passport': {
                'stamps': passport.stamps,
                'activated': passport.activated,
                'donations': passport.donations,
                'recharged': passport.recharged,
                'id': passport.id,
                'first_recharge': passport.first_recharge,
                'rechargeValue': rechargeValue,
                'amount_recharged' : passport.amount_recharged,
                'event_id': passport.event_id
              }
           }


  @jwt_belongsToGroup("Admin")
  def delete(self):
    return { success: True }, 200

  def post(self):
    json = createPassport.parse_args()
    user_id = json["user_id"]
    event_id = json["event_id"]
    passport = Passport(user_id = user_id, event_id = event_id)
    db.session.add(passport)
    db.session.commit()
    return { 'success': True }, 201


class PassportActivation(Resource):

  def get(self, id):
    if not hasPermission("canActivate"):
      return { 'success': False, 'message': InvalidToken }, 401
    passport = Passport.query.filter_by(id=id).first()
    if passport is None:
      return { 'success': False, 'message': PassportNotFound(id) }, 400
    if passport.activated:
      return { 'success': False, 'message': PassportAlreadyActivated }, 201
    if passport.recharged:
      return { 'success': False, 'message': PassportWasRecharged }, 201

    return {'success': True, 'duff_value': passport.event.duff_value}

  @jwt_hasPermission("canActivate")
  def post(self):
    json = passportOperation.parse_args()
    passport = Passport.query.filter_by(id=json["id"]).first()
    first_recharge = json['first_recharge']
    if first_recharge is None:
      return { 'success': False, 'message': 'Error: Bad Argument. Mission \'first_recharge\'' }, 400
    if passport is None:
      return { 'success': False, 'message': PassportNotFound(id) }, 400
    if passport.activated:
      return { 'success': False, 'message': PassportAlreadyActivated }, 201
    if passport.recharged:
      return { 'success': False, 'message': PassportWasRecharged }, 201
    passport.activated = True
    passport.first_recharge = first_recharge
    db.session.commit()
    return { 'success':True }, 200


class PassportRecharge(Resource):
  @jwt_hasPermission("canRecharge")
  def post(self):
    json = passportOperation.parse_args()
    passport = Passport.query.filter_by(id=json["id"]).first()
    if not passport.activated:
      return { 'success': False, 'message': PassportNotActivated }, 201
    if passport.recharged:
      return { 'success': False, 'message': PassportWasRecharged }, 201
    passport.activated = False
    passport.recharged = True
    donations = 0 if passport.donations == 0 else passport.donations + 1
    passport.amount_recharged = passport.event.duff_value * (passport.stamps + donations)
    passport.recharged_by = User.query.filter_by(id = get_jwt_identity()['id']).first().id
    db.session.commit()
    return { 'success': True }, 200

class PassportStamp(Resource):
  @jwt_hasPermission('canStamp')
  def post(self):
    json = passportStamp.parse_args()
    passport = Passport.query.filter_by(id=json["id"]).first()
    if passport is None:
      return { 'success': False, 'message': PassportNotFound(json["id"]) }, 201
    if not passport.activated:
      return { 'success': False, 'message': PassportNotActivated }, 201
    stamps = float(json['stamps'])
    
    isDonation = bool(json['isDonation'])
    socialStamp = bool(json['socialStamp'])

    if isDonation:
      passport.donations += stamps
    else:
      passport.stamps += stamps

    if socialStamp:
      passport.stamps += 0.25

    purchase = Purchase(donation=isDonation, rrss=socialStamp, passport_id = passport.id)
    db.session.add(purchase)
    db.session.commit()

    buyToVendor = BuysToVendor( purchase_id=purchase.id,
                                vendor_id=json["vendor_id"],
                                stamps=stamps,
                                price=stamps * passport.event.duff_value,
                                user_id = get_jwt_identity()["id"] )
    db.session.add(buyToVendor)
    db.session.commit()
    return { 'success': True }, 200

# Router
api.add_resource(PassportList, '/passports')
api.add_resource(PassportController, '/passport/<string:id>', '/passport')
api.add_resource(PassportActivation, '/activate/passport/<string:id>', '/activate/passport')
api.add_resource(PassportRecharge, '/passport/recharge')
api.add_resource(PassportStamp, '/passport/stamp')


