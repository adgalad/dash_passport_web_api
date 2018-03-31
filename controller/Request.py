from flask_restful import reqparse

createUser = reqparse.RequestParser(bundle_errors=True)
createUser.add_argument('firstName', required=True, location='json')
createUser.add_argument('lastName', required=True, location='json')
createUser.add_argument('email',required=True, location='json')
createUser.add_argument('password',required=True, location='json')
createUser.add_argument('id',required=True, location='json')

login = reqparse.RequestParser(bundle_errors=True)
login.add_argument('email', required=True, location='json')
login.add_argument('password', required=True, location='json')