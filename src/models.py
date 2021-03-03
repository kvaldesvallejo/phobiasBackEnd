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
            "profile_picture" : self.profile_picture,
            "account_type" : self.account_type, 
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Therapist(db.Model):
    #int FK >- User.id
    user_id = db.Column(db.Integer, primary_key=True)
    ofice_location = db.Column(db.String(30), unique=False, nullable=False)
    experience = db.Column(db.String(500), unique=False, nullable=False)
    languages_spoke = db.Column(db.String(300), unique=False, nullable=False)

    def __repr__(self):
        return '<Therapist %r>' % self.user_id

    def serialize(self):
        return {
            "user_id": self.user_id,
            "ofice_location" : self.ofice_location,
            "experience" : self.experience,
            "languages_spoke" : self.languages_spoke,
        }

class Patient(db.Model):
    #int FK >- User.id
    user_id = db.Column(db.Integer, primary_key=True)
    wishfearLESS = db.Column(db.String(300), unique=False, nullable=True)
    previous_help = db.Column(db.Boolean, unique=False, nullable=True)
    zc = db.Column(db.Integer, unique=False, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.user_name

    def serialize(self):
        return {
            "user_id": self.user_id,
            "wishfearLESS" : self.wishfearLESS,
            "previous_help" : self.previous_help,
            "zc" : self.zc,
        }