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
from models import db, User, Therapist , Patient, PatientLesson, Lesson

import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config( 
  cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'), 
  api_key = os.environ.get('CLOUDINARY_API_KEY'), 
  api_secret = os.environ.get('CLOUDINARY_API_SECRET') 
)

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

# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200

#-----------------USER-----------------------------------------------------------
# Create a new user 
@app.route('/user', methods=['POST'])
def create_user():
    body = request.get_json()
    #@profile_picture = request.files["profile_picture"]
    
    # if body is None:
    #     raise APIException("You need to specify the request body as a json object", 400)

    # # Validations
    # #First Name
    # if "first_name" in body:
    fn = body['first_name']
    # else:
    #     raise APIException("You need to specify the first name", 400)
    # #Last name
    # if "last_name" in body:
    ln = body['last_name']
    # else:
    #     raise APIException("You need to specify an Last Name", 400)
    # #email
    # if "email" in body:
    e= body["email"]
    # else:
    #     raise APIException("You need to specify an email", 400)
    # if User.query.filter_by(email=body['email']).first() is not None:
    #     raise APIException("email is in use", 400)
    # #phone_number
    # if "phone_number" in body:
    phn = body["phone_number"]
    # else:
    #     raise APIException("You need to specify an phone_number", 400)
    # if User.query.filter_by(phone_number=body['phone_number']).first() is not None:
    #     raise APIException("phone_number is in use", 400)
    # #user_name
    # if "user_name" in body:
    un = body["user_name"]
    # else:
    #     raise APIException("You need to specify an user_name", 400)
    # if User.query.filter_by(user_name=body['user_name']).first() is not None:
    #     raise APIException("user name is in use", 400)
    # #password
    # if "password" in body:
    p = body["password"]
    # else:
    #     raise APIException("You need to specify an password", 400)
    
    #profile_picture
    #if "profile_picture" is not None:
        #pp = request.files["profile_picture"]
        # pp = "---------------"
        # print("---------------------------------------------------")
        #print(profile_picture)
        #picture_uploaded = cloudinary.uploader.upload(profile_picture)
            # options = {
            #            “use_filename”: True  # use filename as public id on cloudinary
            #         })
        #pp = picture_uploaded['secure_url']
    # else:
    #     print("************************************************")
    pp = "default"

    # #account_type
    # if "account_type" in body:
    at = body["account_type"]
    # else:
    #     at="0"

    new_user = User(first_name = fn, 
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

    user = User.query.filter_by(email=e).first()
    print(user)

    #response_body = list(map(lambda x: x.serialize(), user))
    return jsonify(user.serialize()), 200

# Get all users
@app.route('/user', methods=['GET'])
def get_users():

    users = User.query.all()
    response_body = list(map(lambda x: x.serialize(), users))
    #print(response_body)
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
    if "first_name" in body:
        target_user.first_name = body['first_name']
    
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
        
        target_user.profile_picture = request.FILES["profile_picture"]
        print("_______________________")
        print(request.files["profile_picture"])
        picture_uploaded = cloudinary.uploader.upload(target_user.profile_picture)
       
            #options = {
                #        “use_filename”: True  # use filename as public id on cloudinary
                #    })
        target_user.profile_picture = picture_uploaded['secure_url']
    else:
        print("******************************************")

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
@app.route('/therapist', methods=['GET'])
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

#-------------------------Patient---------------------------------------------------
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
    #phobia
    if "phobia" in body:
        p = body["phobia"]
    #wishfearless
    if "wishfearless" in body:
        w = body["wishfearless"]
    #previous_help
    if "previous_help" in body:
        ph = body["previous_help"]
    #severity
    if "severity" in body:
        s = body["severity"]

    new_patient = Patient(user_id = ui, 
                    phobia = p,
                    wishfearless = w, 
                    previous_help = ph, 
                    severity = s)

    db.session.add(new_patient)
    db.session.commit()

    patients = Patient.query.all()
    response_body = list(map(lambda x: x.serialize(), patients))
    return jsonify(response_body), 200

# Get all Patient
@app.route('/patient', methods=['GET'])
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

    #phobia
    if "phobia" in body:
       target_patient.phobia = body['phobia']
    
    #wishfearless
    if "wishfearless" in body:
       target_patient.wishfearless = body['wishfearless']
    
    #previous_help
    if "previous_help" in body:
        target_patient.previous_help = body['previous_help']
   
    #severity
    if "severity" in body:
        target_patient.severity = body['severity']

    db.session.commit()

    patients = Patient.query.all()
    response_body = list(map(lambda x: x.serialize(), patients))
    return jsonify(response_body), 200

#--------------------------Lesson---------------------------------------------------------
# Get all Lesson
@app.route('/lesson', methods=['GET'])
def get_lesons():
    lessons = Lesson.query.all()
    response_body = list(map(lambda x: x.serialize(), lessons))
    return jsonify(response_body), 200

# Create a new Lesson 
@app.route('/lesson', methods=['POST'])
def create_lesson():

    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", 400)

    # Validations
    #name
    if "name" in body:
        n = body["name"]
    else:
        raise APIException("You need to specify the name", 400)
    #phobia_description
    if "phobia_description" in body:
        pd = body["phobia_description"]
    else:
        pd = ""
    #description_1
    if "description_1" in body:
        d1 = body["description_1"]
    else:
        d1 = ""
    #img_2
    if "img_2" in body:
        i2 = body["img_2"]
    else:
        i2 = ""
    #description_2
    if "description_2" in body:
        d2 = body["description_2"]
    else:
        d2 = ""
    #description_3
    if "description_3" in body:
        d3 = body["description_3"]
    else:
        d3 = ""
    #search_3
    if "search_3" in body:
        s3 = body["search_3"]
    else:
        s3 = ""
    #img_4
    if "img_4" in body:
        i4 = body["img_4"]
    else:
        i4 = ""
    #description_4
    if "description_4" in body:
        d4 = body["description_4"]
    else:
        d4 = ""
    #img_5
    if "img_5" in body:
        i5 = body["img_5"]
    else:
        i5 = ""
    #description_5
    if "description_5" in body:
        d5 = body["description_5"]
    else:
        d5 = ""
    #search_5
    if "search_5" in body:
        s5 = body["search_5"]
    else:
        s5 = ""
    #description_6
    if "description_6" in body:
        d6 = body["description_6"]
    else:
        d6 = ""
        #raise APIException("You need to specify the description 6", 400)
    
    new_lesson = Lesson(name = n, 
                    phobia_description = pd, 
                    description_1 = d1, 
                    img_2 = i2,
                    description_2 = d2,
                    description_3 = d3,
                    search_3 = s3,
                    img_4 = i4,
                    description_4 = d4,
                    img_5 = i5,
                    description_5 = d5,
                    search_5 = s5, 
                    description_6 = d6,
                    )

    db.session.add(new_lesson)
    db.session.commit()

    lessons = Lesson.query.all()
    response_body = list(map(lambda x: x.serialize(), lessons))
    return jsonify(response_body), 200

#-------------------------PatientLesson-------------------------------------------------
# Get all PatientLesson
@app.route('/patientlesson', methods=['GET'])
def get_patient_lesson():
    patientlessons = PatientLesson.query.all()
    response_body = list(map(lambda x: x.serialize(), patientlessons))
    return jsonify(response_body), 200

# Create a new Lesson 
@app.route('/patientlesson', methods=['POST'])
def create_patient_lesson():

    body = request.get_json()
    if body is None:
        raise APIException("You need to specify the request body as a json object", 400)

    # Validations
    #id_lesson
    if "id_lesson" in body:
        il = body["id_lesson"]
    else:
        raise APIException("You need to specify the id_lesson", 400)
    #id_patient
    if "id_patient" in body:
        ip = body["id_patient"]
    else:
        raise APIException("You need to specify the id_patient", 400)
    #question_2_feeling
    if "question_2_feeling" in body:
        q2f = body["question_2_feeling"]
    else:
        q2f = ""
    #question_2_experience
    if "question_2_experience" in body:
        q2e = body["question_2_experience"]
    else:
        q2e = ""
    #question_2_date
    if "question_2_date" in body:
        q2d = body["question_2_date"]
    else:
        q2d = ""

    #question_4_feeling
    if "question_4_feeling" in body:
        q4f = body["question_4_feeling"]
    else:
        q4f = ""
    #question_4_experience
    if "question_4_experience" in body:
        q4e = body["question_4_experience"]
    else:
        q4e = ""
    #question_4_date
    if "question_4_date" in body:
        q4d = body["question_4_date"]
    else:
        q4d = ""
    #description_4
    if "description_4" in body:
        d4 = body["description_4"]
    else:
        d4 = ""

    #question_5_feeling
    if "question_5_feeling" in body:
        q5f = body["question_5_feeling"]
    else:
        q5f = ""
    #question_5_experience
    if "question_5_experience" in body:
        q5e = body["question_5_experience"]
    else:
        q5e = ""
    #question_5_date
    if "question_5_date" in body:
        q5d = body["question_5_date"]
    else:
        q5d = ""
       
    #actual_step
    if "actual_step" in body:
        ast = body["actual_step"]
    else:
        ast = 0
    
    new_patient_lesson = PatientLesson(name = n, 
                    id_lesson = il, 
                    id_patient = ip, 
                    question_2_feeling = q2f,
                    question_2_experience = q2e,
                    question_2_date = q2d,
                    question_4_feeling = q4f,
                    question_4_experience = q4e,
                    question_4_date = q4d,
                    question_5_feeling = q5f,
                    question_5_experience = q5e,
                    question_5_date = q5d, 
                    actual_step = ast,
                    )

    db.session.add(new_patient_lesson)
    db.session.commit()

    new_patient_lessons = PatientLesson.query.all()
    response_body = list(map(lambda x: x.serialize(), new_patient_lessons))
    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
