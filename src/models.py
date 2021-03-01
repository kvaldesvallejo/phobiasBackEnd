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