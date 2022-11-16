from main import db, ma

class Booking(db.Model):
    __tablename__ = 'bookings'

    id =db.column(db.Integer, primary_key=True)
    date = db.column(db.Date, nullable=False)
    time = db.column(db.Time, nullable=False)

    dive_trip_id = db.Column(db.Integer, db.ForeignKey("dive_trips.id"), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    dive_trip = db.relationship("DiveTrip", back_populates="bookings")
    client = db.relationship("Client", back_populates="bookings")

    class BookingSchema(ma.Schema):
        class Meta:
            fields = ('id', 'date', 'time', 'dive_trips_id', 'client_id')
            ordered = True

