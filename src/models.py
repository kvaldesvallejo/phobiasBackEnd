from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fisrt_name = db.Column(db.String(10), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    profile_picture = db.Column(db.String(120), nullable=True)
    account_type = db.Column(db.Integer, unique=False, nullable=False) 
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.user_name

    def serialize(self):
        return {
            "id": self.id,
            "fisrt_name" : self.fisrt_name,
            "last_name" : self.last_name,
            "phone_number" : self.phone_number,
            "user_name" : self.user_name,
            "account_type" : self.account_type, 
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Therapist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    ofice_location = db.Column(db.String(30), unique=False, nullable=False)
    experience = db.Column(db.String(500), unique=False, nullable=False)
    languages_spoke = db.Column(db.String(300), unique=False, nullable=False)

    def __repr__(self):
        return '<Therapist %r>' % self.user_id

    def serialize(self):
        return {
            "id" : self.id,
            "user_id": self.user_id,
            "ofice_location" : self.ofice_location,
            "experience" : self.experience,
            "languages_spoke" : self.languages_spoke,
        }

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    wishfearLESS = db.Column(db.String(300), unique=False, nullable=True)
    previous_help = db.Column(db.Boolean, unique=False, nullable=True)
    zc = db.Column(db.Integer, unique=False, nullable=True)

    def __repr__(self):
        return '<Patient %r>' % self.user_id

    def serialize(self):
        return {
            "id" : self.id,
            "user_id": self.user_id,
            "wishfearLESS" : self.wishfearLESS,
            "previous_help" : self.previous_help,
            "zc" : self.zc,
        }

class Testimonial(db.Model):
    #int FK >- User.id
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    desciption = db.Column(db.String(300), unique=False, nullable=True)
    testimonial_photo = db.Column(db.String(500), unique=False, nullable=True)

    def __repr__(self):
        return '<Testimonial %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id" : self.user_id,
            "desciption" : self.desciption
        }

class PatienPhobia(db.Model):
    #int FK >- User.id
    id_phobia_lesson = db.Column(db.Integer, primary_key=True)
    id_patient = db.Column(db.Integer, unique=False, nullable=False)
    #FK >- Question.id
    question_2 = db.Column(db.Integer, unique=False, nullable=True)
    #FK >- Question.id
    question_4 = db.Column(db.Integer, unique=False, nullable=True)
    #FK >- Question.id
    question_5 = db.Column(db.Integer, unique=False, nullable=True)
    actual_step = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<PatienPhobia %r>' % self.id_phobia_lesson

    def serialize(self):
        return {
            "id_phobia_lesson": self.id_phobia_lesson,
            "id_patient" : self.id_patient,
            "question_2" : self.question_2,
            "question_4" : self.question_4,
            "question_5" : self.question_5,
            "actual_step" : self.actual_step
        }

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feeling = db.Column(db.String(300), unique=False, nullable=True)
    experience = db.Column(db.String(300), unique=False, nullable=True)
    step = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Question %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "feeling" : self.feeling,
            "experience" : self.experience,
            "step" : self.step
        }

class PhobiaLesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=False, nullable=False)
    phobia_description = db.Column(db.String(500), unique=False, nullable=False)
    description_1 = db.Column(db.String(500), unique=False, nullable=False)
    img_2 = db.Column(db.String(500), unique=False, nullable=False)
    description_2 = db.Column(db.String(500), unique=False, nullable=False)
    question_2 = db.Column(db.String(500), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.user_name

    def serialize(self):
        return {
            "id": self.id,
            "fisrt_name" : self.fisrt_name,
            "last_name" : self.last_name,
            "phone_number" : self.phone_number,
            "user_name" : self.user_name,
            "account_type" : self.account_type, 
            "email": self.email,
            # do not serialize the password, its a security breach
        }

# 3_description string
# 3_search string
# 4_img string
# 4_description string
# 4_question
# 5_img string
# 5_description string
# 5_quetion
# 5_search string
# 6_description string
