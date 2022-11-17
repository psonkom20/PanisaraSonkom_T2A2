from init import db, ma
from marshmallow.validate import OneOf, And, Regexp

VALID_DIVE_LEVEL = ('Open-water','Advanced', 'Rescue', 'Dive-Master')

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), nullable = False, unique= True)
    password = db.Column(db.String, nullable = False)
    dive_level = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default = False)

    bookings =db.relationship('Booking', back_populates= 'users', cascade= 'all, delete')

class UserSchema(ma.Schema):

    dive_level = fields.String(required=True, validate=And(
        OneOf(VALID_DIVE_LEVEL), Regexp('[a-zA-Z0-9]+$', error= 'Only letters, numbers and spaces are allowed')))

    class Meta:
        fields = ('id', 'name', 'email', 'dive_level', 'is_admin', 'password')
        ordered = True