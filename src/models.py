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

    user_therapist = db.relationship("Therapist", uselist=False, backref="user")
    user_patient = db.relationship("Patient", uselist=False, backref="user")
    testimonial = db.relationship("Testimonial", uselist=False, backref="user")

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
            #"user_therapist": self.user_therapist.serialize() if self.therapist else None,
            #"user_patient": self.user_patient.serialize() if not self.therapist else None,
            # do not serialize the password, its a security breach
        }

class Therapist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
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
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    wishfearLESS = db.Column(db.String(300), unique=False, nullable=True)
    previous_help = db.Column(db.Boolean, unique=False, nullable=True)
    zc = db.Column(db.Integer, unique=False, nullable=True)

    patient_lesson = db.relationship("PatientLesson", uselist=False, backref="patient")

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
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    desciption = db.Column(db.String(300), unique=False, nullable=True)
    testimonial_photo = db.Column(db.String(500), unique=False, nullable=True)
    date = db.Column(db.String(15), unique=False, nullable=False)

    def __repr__(self):
        return '<Testimonial %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id" : self.user_id,
            "desciption" : self.desciption,
            "date" : self.date
        }

class PatientLesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_lesson = db.Column(db.Integer, db.ForeignKey("lesson.id"), nullable=False)
    id_patient = db.Column(db.Integer, db.ForeignKey("patient.id"))
    question_2 = db.Column(db.Integer, db.ForeignKey("question.id"))
    #question_4 = db.Column(db.Integer, db.ForeignKey("question.id"))
    #question_5 = db.Column(db.Integer, db.ForeignKey("question.id"))
    actual_step = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Patien_lesson %r>' % self.id

    def serialize(self):
        return {
            "id": self.os,
            "id_lesson": self.id_lesson,
            "id_patient" : self.id_patient,
            "question_2" : self.question_2,
            #"question_4" : self.question_4,
            #"question_5" : self.question_5,
            "actual_step" : self.actual_step
        }

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feeling = db.Column(db.String(300), unique=False, nullable=True)
    experience = db.Column(db.String(300), unique=False, nullable=True)
    step = db.Column(db.Integer, unique=False, nullable=False)
    date = db.Column(db.String(15), unique=False, nullable=False)

    patient_phobia = db.relationship("PatientLesson", uselist=False, backref="question")

    def __repr__(self):
        return '<Question %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "feeling" : self.feeling,
            "experience" : self.experience,
            "step" : self.step,
            "date" : self.date
        }

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=False, nullable=False)
    phobia_description = db.Column(db.String(500), unique=False, nullable=False)
    description_1 = db.Column(db.String(500), unique=False, nullable=False)
    img_2 = db.Column(db.String(500), unique=False, nullable=False)
    description_2 = db.Column(db.String(500), unique=False, nullable=False)
    question_2 = db.Column(db.Integer, unique=False, nullable=False)
    description_3 = db.Column(db.String(500), unique=False, nullable=False)
    search_3 = db.Column(db.String(500), unique=False, nullable=False)
    img_4 = db.Column(db.String(500), unique=False, nullable=False)
    description_4 = db.Column(db.String(500), unique=False, nullable=False)
    question_4 = db.Column(db.Integer, unique=False, nullable=False)
    img_5 = db.Column(db.String(500), unique=False, nullable=False)
    description_5 = db.Column(db.String(500), unique=False, nullable=False)
    question_5 = db.Column(db.Integer, unique=False, nullable=False)
    search_5 = db.Column(db.String(500), unique=False, nullable=False)
    description_6 = db.Column(db.String(500), unique=False, nullable=False)

    patient_phobia = db.relationship("PatientLesson", backref="lesson", uselist=False) 

    def __repr__(self):
        return '<Lesson %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name" : self.name,
            "phobia_description" : self.phobia_description,
            "description_1" : self.description_1,
            "img_2" : self.img_2,
            "description_2" : self.description_2, 
            "question_2": self.question_2,
            "description_3": self.description_3,
            "search_3": self.search_3,
            "img_4": self.img_4,
            "description_4": self.description_4,
            "question_4": self.question_4,
            "img_5": self.img_5,
            "description_5": self.description_5,
            "question_5": self.question_5,
            "search_5": self.search_5,
            "description_6": self.description_6,

        }

