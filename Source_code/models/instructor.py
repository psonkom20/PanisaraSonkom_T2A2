from init import db, ma

class Instructor(db.Model):
    __tablename__ = 'instructors'

    id = db.Column(db.Integer, primary_key=True)
    specialties = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)

    users = db.relationship('User', back_populates='instructors')
    dive_trips = db.relationship('DiveTrip', back_populates='instructors', cascade= 'all, delete')

class InstructorSchema(ma.Schema):
    fields = ('id', 'specialties', 'user_id')
    ordered = True
