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


# Passport
createPassport = reqparse.RequestParser(bundle_errors=True)
createPassport.add_argument('user_id', required=True, location='json')