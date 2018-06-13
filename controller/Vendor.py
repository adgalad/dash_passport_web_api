
from models.db import db
from models.User import User
from models.Passport import Passport
from models.Event import Event
from models.Vendor import Vendor, Product, Purchase, product_purchase_table
from controller.Language import *
from controller.Permission import belongsToGroup, hasPermission, isCurrentUser, jwt_belongsToGroup
from controller.Request import createVendor, registerSell, updateProduct, createProduct

from flask_restful import Resource
from App import app, api
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime
import time
import json as Json




# List Users
# class VendorList(Resource):
#   @jwt_belongsToGroup("Admin")
#   def get(self):
#     response = []
#     for event in Event.query.all():
#       response.append(str(event))
#     return {'success': True, "events": response}



# User (post: Create, get: Show, put: Modify, delete: Delete)
class VendorController(Resource):

  def get(self, id):
    vendor = Vendor.query.filter_by(id = id).first()


    return { 'success': True, "name" : vendor.name }, 200


  @jwt_belongsToGroup("Admin")
  def put(self):

    return { 'success': True }, 200

  def post(self):
    json = createVendor.parse_args()
    vendor = Vendor(name=json["name"], event_id=json["event_id"])
    db.session.add(vendor)
    db.session.commit()
    return { 'success': True }, 201

class VendorSells(Resource):
  def get(self, id):
    vendor = Vendor.query.filter_by(id=id).first()
    if vendor is None:
      return {'success': False, 'message':"Vendor doesn't exists"}, 400

    purchases = sorted(vendor.purchases, key=lambda x: x.datetime, reverse=True)

    response = []
    for p in purchases:
      response.append({ 'name':str(p), 'price':p.price, 'datetime':p.datetime.timestamp()})
    return {'success': True, 'purchases':response}, 200

  def post(self):
    json = registerSell.parse_args()
# registerSell.add_argument('vendor_id', required=True, location='json')
# registerSell.add_argument('passport_id', required=True, location='json')
# registerSell.add_argument('value', required=True, location='json')
# registerSell.add_argument('products', required=True, location='json')
# registerSell.add_argument('client_id', required=True, location='json')
    print(json['products'])
    try:
      products = Json.loads(json['products'])
    except Exception as e:
      return {'success': False, 'message': 'Bad product json\n%s' % str(e)}, 400

    passport = Passport.query.filter_by(user_id=json['client_id'], event_id=json['event_id']).first()
    if passport is None:
      event = Event.query.filter_by(id=json['event_id']).first()
      if event is None:
        return {'success': False, 'message':EventDoesntExist}, 400
      passport = event.passport_id
    else:
      passport = passport.id

    
    vendor = Vendor.query.filter_by(id=json['vendor_id']).first()
    if vendor is None:
      return {'success': False, 'message':"Vendor doesn't exists"}, 400

    purchase = Purchase(donation = vendor.isFoundation,
                        passport_id = passport,
                        id_client = json['client_id'],
                        price = json['value'],
                        vendor = vendor)
    db.session.add(purchase)
    db.session.commit()
    vendorProducts = Product.query.filter_by(vendor_id=json['vendor_id'])

    updates = []
    for i in products:
      p = vendorProducts.filter_by(name=i).first()
      purchase.products.append(p)
      p.purchases.append(purchase)
      db.session.commit()
      r = product_purchase_table.update().\
                  where(product_purchase_table.c.purchase_id == purchase.id).\
                  where(product_purchase_table.c.product_id == p.id).\
                  values(amount = products[i])
      updates.append(r)

    for i in updates:
      db.session.execute(i)
    
    db.session.commit()
    return {'success':True}, 200

class VendorProducts(Resource):
  def get(self, id):
    vendor = Vendor.query.filter_by(id=id).first()
    products = vendor.products
    response = []
    for i in products:
      response.append({"name":i.name, "price":i.price, "id": i.id})

    return {"success":True, "products":response}, 201

  def post(self):
    json = createProduct.parse_args()

    # vendor = Vendor.query.filter_by(id=json['id']).first()

    # if vendor is None:
    #   return {"success":False, "message": VendorDoesntExist}, 400

    product = Product.query.filter_by(name = json['name'], vendor_id=json['id']).first()
    if product is None:
      product = Product(name = json['name'], price=json['price'], vendor_id=json['id'])
      db.session.add(product)
      db.session.commit()
      p = {"name": product.name, "price": product.price, "id": product.id}
      return {"success":True, "product":p}, 200
    else:
      return {"success":False, "message": "Ya existe el producto"}, 400

  def put(self):
    json = updateProduct.parse_args()

    vendor = Vendor.query.filter_by(id=json['id']).first()

    # if vendor is None:
    #   return {"success":False, "message": VendorDoesntExist}, 400

    product = Product.query.filter_by(id = json['product_id'], vendor_id=json['id']).first()
    if product is None:
      return {"success":False, "message": "Error"}, 400
    else:
      product.name = json['name']
      product.price = json['price']
      db.session.commit()
      return {"success":True, "message": ProductChanged}, 200

# Router
# api.add_resource(EventList, '/events')
api.add_resource(VendorController, '/vendor/<string:id>', '/vendor')
api.add_resource(VendorSells, '/vendor/registerSell', '/vendor/<string:id>/sells')
api.add_resource(VendorProducts, '/vendor/<string:id>/products', '/vendor/products')
