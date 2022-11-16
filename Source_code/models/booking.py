from init import db, ma

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    dive_trip_id = db.Column(db.Integer, db.ForeignKey('dive_trips.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    dive_trips = db.relationship('DiveTrip', back_populates='bookings', cascade= 'all, delete')
    clients = db.relationship('Client', back_populates='bookings')

class BookingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date', 'time', 'dive_trip_id', 'client_id')
        ordered = True

