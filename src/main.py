"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User

#import cloudinary
#import cloudinary.uploader
#import cloudinary.api

#cloudinary.config( 
 # cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'), 
  #api_key = os.environ.get('CLOUDINARY_API_KEY'), 
  #api_secret = os.environ.get('CLOUDINARY_API_SECRET') 
#)

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# Create a new user 
@app.route('/user', methods=['POST'])
def create_user():
    body = request.get_json()
    #print(  request)
    #print(  body)
    
    if body is None:
        raise APIException("You need to specify the request body as a json object", 400)

    # Validations
    #First Name
    if "fisrt_name" in body:
        #print ("fisrt_name[" + str(body['fisrt_name']) +"]")
        fn = body['fisrt_name']
    else:
        raise APIException("You need to specify the first name", 400)
    #Last name
    if "last_name" in body:
        ln = body['last_name']
        #user["last_name"] = body["last_name"]
    else:
        raise APIException("You need to specify an Last Name", 400)
    #email
    if "email" in body:
        e= body["email"]
    else:
        raise APIException("You need to specify an email", 400)
    if User.query.filter_by(email=body['email']).first() is not None:
        raise APIException("email is in use", 400)

    #phone_number
    if "phone_number" in body:
        phn = body["phone_number"]
    else:
        raise APIException("You need to specify an phone_number", 400)
    if User.query.filter_by(phone_number=body['phone_number']).first() is not None:
        raise APIException("phone_number is in use", 400)

    #user_name
    if "user_name" in body:
        un = body["user_name"]
    else:
        raise APIException("You need to specify an user_name", 400)
    if User.query.filter_by(user_name=body['user_name']).first() is not None:
        raise APIException("user name is in use", 400)

    #password
    if "password" in body:
        p = body["password"]
    else:
        raise APIException("You need to specify an password", 400)
    if User.query.filter_by(password=body['password']).first() is not None:
        raise APIException("password is in use", 400)

    #profile_picture
    if "profile_picture" in body:
        pp = body["profile_picture"]
    else:
        pp = "default"

    #account_type
    if "account_type" in body:
        at = body["account_type"]
    else:
        raise APIException("You need to specify the account_type", 400)

    new_user = User(fisrt_name = fn, 
                    last_name = ln, 
                    email= e, 
                    phone_number = phn, 
                    user_name = un, 
                    password = p, 
                    profile_picture = pp, 
                    account_type = at)

    print(new_user)

    db.session.add(new_user)
    db.session.commit()

    users = User.query.all()
    response_body = list(map(lambda x: x.serialize(), users))
    #print(response_body)
    #print(users)
    return jsonify(response_body), 200

@app.route('/users', methods=['GET'])
def get_users():

    users = User.query.all()
    response_body = list(map(lambda x: x.serialize(), users))
    print(response_body)
    print(users)
    return jsonify(response_body), 200    

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
