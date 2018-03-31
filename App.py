
# Flask
from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from controller.Language import *

from flask_admin import Admin


# address = "ec2-18-219-254-206.us-east-2.compute.amazonaws.com"
address = "localhost"
host = "http://" + address +":5001"



app = Flask('application/json')
app.config['BUNDLE_ERRORS'] = True
CORS(app)

# Flask_Admin. It gives us an **Ugly** admin interface.
admin = Admin(app, name="console", template_mode='bootstrap3')


# SQLAlchemy config variables
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Flask_restful
api = Api(app)


# Flask-mail 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'smarticket.suport@gmail.com'
app.config['MAIL_PASSWORD'] = 'asd123asd'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)



# Application secret for encoding
app.secret_key = "EsTa_3S_L4_C74V3_D3_L4_44P"
app.config['JWT_SECRET_KEY'] = app.secret_key



# Flask_JWT gives an mechanism to handle JSON Web Tokens
jwt = JWTManager(app)
# JWT error messages overloading
@jwt.expired_token_loader
def expired_token_callback(s):
    return jsonify({'message': ExpiredToken}), 401

@jwt.invalid_token_loader
def invalid_token_callback(s):
    return jsonify({'message': InvalidToken}), 401

@jwt.unauthorized_loader
def unauthorized_callback(s):
    return jsonify({'message': UnauthorizedToken}), 401
