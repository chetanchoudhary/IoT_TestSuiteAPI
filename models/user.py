from db import db


class UserModel(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60))
    password = db.Column(db.String(60))
    access = db.Column(db.String(10))
    firstName = db.Column(db.String(20))
    lastName = db.Column(db.String(20))
    contactNumber = db.Column(db.Integer)

    def __init__(self, email, password, access, firstName, lastName, contactNumber):
        self.email = email
        self.password = password
        self.access = access
        self.firstName = firstName
        self.lastName = lastName
        self.contactNumber = contactNumber

    def json(self):
        return {"email": self.email, "access": self.access, "name": self.firstName + " " + self.lastName, "contact": self.contactNumber}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
