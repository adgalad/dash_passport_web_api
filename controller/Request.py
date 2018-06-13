from flask_restful import reqparse

# User
createUser = reqparse.RequestParser(bundle_errors=True)
createUser.add_argument('firstName', required=True, location='json')
createUser.add_argument('lastName', required=True, location='json')
createUser.add_argument('email',required=True, location='json')
createUser.add_argument('password',required=True, location='json')
createUser.add_argument('id',required=True, location='json')

login = reqparse.RequestParser(bundle_errors=True)
login.add_argument('email', required=True, location='json')
login.add_argument('password', required=True, location='json')

modifyUser = reqparse.RequestParser(bundle_errors=True)
modifyUser.add_argument('firstName', required=False, location='json')
modifyUser.add_argument('lastName', required=False, location='json')
modifyUser.add_argument('email', required=False, location='json')
modifyUser.add_argument('password', required=False, location='json')
modifyUser.add_argument('id', required=True, location='json')

# Passport
createPassport = reqparse.RequestParser(bundle_errors=True)
createPassport.add_argument('user_id', required=True, location='json')
createPassport.add_argument('event_id', required=True, location='json')

passportOperation = reqparse.RequestParser(bundle_errors=True)
passportOperation.add_argument('id', required=True, location='json')
passportOperation.add_argument('first_recharge', required=False, location='json')

passportStamp = reqparse.RequestParser(bundle_errors=True)
passportStamp.add_argument('id', required=True, location='json')
passportStamp.add_argument('vendor_id', required=True, location='json')
passportStamp.add_argument('stamps', required=True, location='json')
passportStamp.add_argument('isDonation', location='json')
passportStamp.add_argument('socialStamp', location='json')


#Event
createEvent = reqparse.RequestParser(bundle_errors=True)
createEvent.add_argument('name', required=True, location='json')
createEvent.add_argument('date', required=True, location='json')
createEvent.add_argument('location', required=True, location='json')
createEvent.add_argument('duff_value', required=True, location='json')

desactivateEvent = reqparse.RequestParser(bundle_errors=True)
desactivateEvent.add_argument('id', required=True, location='json')


# Vendor
createVendor = reqparse.RequestParser(bundle_errors=True)
createVendor.add_argument('name', required=True, location='json')
createVendor.add_argument('event_id', required=True, location='json')

registerSell = reqparse.RequestParser(bundle_errors=True)
registerSell.add_argument('vendor_id', required=True, location='json')
registerSell.add_argument('event_id', required=True, location='json')
registerSell.add_argument('client_id', required=True, location='json')
registerSell.add_argument('value', required=True, location='json')
registerSell.add_argument('products', required=True, location='json')

updateProduct = reqparse.RequestParser(bundle_errors=True)
updateProduct.add_argument('id', required=True, location='json')
updateProduct.add_argument('product_id', required=True, location='json')
updateProduct.add_argument('name', required=True, location='json')
updateProduct.add_argument('price', required=True, location='json')

createProduct = reqparse.RequestParser(bundle_errors=True)
createProduct.add_argument('name', required=True, location='json')
createProduct.add_argument('price', required=True, location='json')
createProduct.add_argument('id', required=True, location='json')