from init import db, ma

class DiveTrip(db.Model):
    __tablename__ = 'dive_trips'

    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, nullable = False)
    dive_lvl_required=db.Column(db.String, nullable = False)
    location= db.Column(db.String, nullable = False)
    date= db.Column(db.String, nullable = False)
    description= db.Column(db.String, nullable = False)
    max_no_people=db.Column(db.Integer, nullable = False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable = False)

    instructors = db.relationship("Instructor", back_populates= 'dive_trips')
    bookings = db.relationship("Booking", back_populates= 'dive_trips')

class DiveTripSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'dive_lvl_required', 'location', 'date', 'description', 'max_no_people', 'instructor_id')
        ordered = True

