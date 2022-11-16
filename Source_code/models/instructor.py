from main import db, ma

class Instructor(db.Model):
    __tablename__ = 'instructors'

    id = db.Column(db.Integer, primary_key=True)
    specialties = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable False)
    user = db.relationship("User", back_populates="instructors")

class InstructorSchema(ma.Schema):
    fields = ('id', 'specialties')
    ordered = True
