from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf, And, Regexp

VALID_DIVE_LVL_REQUIRED = ('Open-water','Advanced')

class DiveTrip(db.Model):
    __tablename__ = 'dive_trips'

    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, nullable = False)
    dive_lvl_required=db.Column(db.String, nullable = False)
    location= db.Column(db.String, nullable = False)
    date= db.Column(db.String, nullable = False)
    description= db.Column(db.String, nullable = False)
    max_no_people=db.Column(db.Integer, nullable = False)

    bookings = db.relationship('Booking', back_populates= 'dive_trips')

class DiveTripSchema(ma.Schema):
    dive_lvl_required = fields.String(required=True, validate=And(
        OneOf(VALID_DIVE_LVL_REQUIRED), Regexp('[a-zA-Z0-9]+$', error= 'Only letters, numbers and spaces are allowed for this field')))

    class Meta:
        fields = ('id', 'name', 'dive_lvl_required', 'location', 'date', 'description', 'max_no_people')
        ordered = True

