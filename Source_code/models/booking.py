from init import db, ma
from marshmallow import fields

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    dive_trip_id = db.Column(db.Integer, db.ForeignKey('dive_trips.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    dive_trips = db.relationship('DiveTrip', back_populates='bookings', cascade= 'all, delete')
    users = db.relationship('User', back_populates='bookings')


class BookingSchema(ma.Schema):

    dive_trips = fields.Nested('DiveTripSchema')
    users = fields.Nested('UserSchema',  exclude=['password'])

    class Meta:
        fields = ('id', 'date', 'time', 'users','dive_trips', '_dive_trip_id','user_id')
        dump_only = ('id', 'date', 'time', 'users','dive_trips')
        load_only = ('id', 'date', 'time', 'user_id', 'dive_trip_id')
        ordered = True

