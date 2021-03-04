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
from models import db, User, Therapist , Patient

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

#-----------------USER-----------------------------------------------------------
# Create a new user 
@app.route('/user', methods=['POST'])
def create_user():
    body = request.get_json()
    
    if body is None:
        raise APIException("You need to specify the request body as a json object", 400)

    # Validations
    #First Name
    if "fisrt_name" in body:
        fn = body['fisrt_name']
    else:
        raise APIException("You need to specify the first name", 400)
    #Last name
    if "last_name" in body:
        ln = body['last_name']
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
    return jsonify(response_body), 200

# Get all users
@app.route('/users', methods=['GET'])
def get_users():

    users = User.query.all()
    response_body = list(map(lambda x: x.serialize(), users))
    print(response_body)
    print(users)
    return jsonify(response_body), 200    

# Get an specific user by id 
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    
    target_user = User.query.get(user_id)
    if target_user is None:
        raise APIException("User not found", 400)

    return jsonify(target_user.serialize(), 200)

# Update an specific user by id 
@app.route('/user/<int:user_id>', methods=['POST'])
def handle_single_user(user_id):

    target_user = User.query.get(user_id)
    if target_user is None:
        raise APIException("User not found", 400)

    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", 400)

    # Validations
    #First Name
    if "fisrt_name" in body:
        target_user.fisrt_name = body['fisrt_name']
    
    #Last name
    if "last_name" in body:
        target_user.last_name = body['last_name']
    
    #email
    if "email" in body:
        if User.query.filter_by(email=body['email']).first() is not None:
            raise APIException("Email is in use", 400)
        target_user.email = body["email"]

    #phone_number
    if "phone_number" in body:
        if User.query.filter_by(phone_number=body['phone_number']).first() is not None:
            raise APIException("phone_number is in use", 400)
        target_user.phone_number = body["phone_number"]

    #user_name
    if "user_name" in body:
        if User.query.filter_by(user_name=body['user_name']).first() is not None:
            raise APIException("user name is in use", 400)
        target_user.user_name = body["user_name"]
    
    #password
    if "password" in body:
        target_user.password = body["password"]
    
    #profile_picture
    if "profile_picture" in body:
        target_user.profile_picture = body["profile_picture"]

    #account_type
    if "account_type" in body:
        target_user.account_type = body["account_type"]
                        
    db.session.commit()
            
    users = User.query.all()
    response_body = list(map(lambda x: x.serialize(), users))
    return jsonify(response_body), 200

#-----------------Therapist-----------------------------------------------------------
# Create a new Therapist 
@app.route('/therapist', methods=['POST'])
def create_therapist():
    body = request.get_json()
    
    if body is None:
        raise APIException("You need to specify the request body as a json object", 400)

    # Validations
    #user_id
    if "user_id" in body:
        ui = body["user_id"]
    else:
        raise APIException("You need to specify an user_id", 400)
    #ofice_location
    if "ofice_location" in body:
        ol = body["ofice_location"]
    else:
        raise APIException("You need to specify an ofice_location", 400)
    #experience
    if "experience" in body:
        e = body["experience"]
    else:
        e = "default"
    #languages_spoke
    if "languages_spoke" in body:
        ls = body["languages_spoke"]
    else:
        raise APIException("You need to specify the languages_spoke", 400)

    new_therapist = Therapist(user_id = ui, 
                    ofice_location = ol, 
                    experience = e, 
                    languages_spoke = ls)

    print(new_therapist)

    db.session.add(new_therapist)
    db.session.commit()

    therapists = Therapist.query.all()
    response_body = list(map(lambda x: x.serialize(), therapists))
    return jsonify(response_body), 200
       
# Get all Therapist
@app.route('/therapists', methods=['GET'])
def get_therapists():
    therapists = Therapist.query.all()
    response_body = list(map(lambda x: x.serialize(), therapists))
    return jsonify(response_body), 200

# Get an specific Therapist by id 
@app.route('/therapist/<int:user_id>', methods=['GET'])
def get_therapist(user_id):
    target_therapists = Therapist.query.get(user_id)
    if target_therapists is None:
        raise APIException("User not found", 400)

    return jsonify(target_therapists.serialize(), 200)

# Update an specific Therapist by id
@app.route('/therapist/<int:user_id>', methods=['POST'])
def update_therapist(user_id):

    target_therapist = User.query.get(user_id)

    if target_therapist is None:
        raise APIException("Therapist not found", 400)

    body = request.get_json()
    
    if body is None:
        raise APIException("You need to specify the request body as a json object", 400)

    # Validations
    #user_id
    if "user_id" in body:
        target_therapist.user_id = body['user_id']
    
    #ofice_location
    if "ofice_location" in body:
       target_therapist.ofice_location = body['ofice_location']
    
    #experience
    if "experience" in body:
        target_therapist.experience = body['experience']
   
    #languages_spoke
    if "languages_spoke" in body:
        target_therapist.languages_spoke = body['languages_spoke']

    db.session.commit()

    therapists = Therapist.query.all()
    response_body = list(map(lambda x: x.serialize(), therapists))
    return jsonify(response_body), 200

#-----------------Patient-----------------------------------------------------------
# Create a new Patient 
@app.route('/patient', methods=['POST'])
def create_patient():

    body = request.get_json()

    if body is None:
        raise APIException("You need to specify the request body as a json object", 400)

    # Validations
    #user_id
    if "user_id" in body:
        ui = body["user_id"]
    else:
        raise APIException("You need to specify an user_id", 400)
    #wishfearLESS
    if "wishfearLESS" in body:
        w = body["wishfearLESS"]
    #previous_help
    if "previous_help" in body:
        ph = body["previous_help"]
    #zc
    if "zc" in body:
        zipc = body["zc"]
    else:
        raise APIException("You need to specify the languages_spoke", 400)

    new_patient = Patient(user_id = ui, 
                    wishfearLESS = w, 
                    previous_help = ph, 
                    zc = zipc)

    db.session.add(new_patient)
    db.session.commit()

    patients = Patient.query.all()
    response_body = list(map(lambda x: x.serialize(), patients))
    return jsonify(response_body), 200

# Get all Patient
@app.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    response_body = list(map(lambda x: x.serialize(), patients))
    return jsonify(response_body), 200

# Get an specific Patient by id 
@app.route('/patient/<int:user_id>', methods=['GET'])
def get_patient_by_id(user_id):
    target_patient = Patient.query.get(user_id)
    if target_patient is None:
        raise APIException("User not found", 400)

    return jsonify(target_patient.serialize(), 200)

# Update an specific Patient by id
@app.route('/patient/<int:user_id>', methods=["PUT"])
def update_patient(user_id):

    target_patient = Patient.query.get(user_id)

    if target_patient is None:
        raise APIException("Patient not found", 400)

    body = request.get_json()
    
    if body is None:
        raise APIException("You need to specify the request body as a json object", 400)

    # Validations
    #user_id
    if "user_id" in body:
        target_patient.user_id = body['user_id']
    
    #wishfearLESS
    if "wishfearLESS" in body:
       target_patient.wishfearLESS = body['wishfearLESS']
    
    #previous_help
    if "previous_help" in body:
        target_patient.previous_help = body['previous_help']
   
    #zc
    if "zc" in body:
        target_patient.zc = body['zc']

    db.session.commit()

    patients = Patient.query.all()
    response_body = list(map(lambda x: x.serialize(), patients))
    return jsonify(response_body), 200



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
