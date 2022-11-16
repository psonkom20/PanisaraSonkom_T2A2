from init import db, ma

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), nullable = False, unique= True)
    password = db.Column(db.String, nullable = False)
    dive_level = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default = False)

    clients = db.relationship('Client', back_populates='users', cascade= 'all, delete', uselist= False)
    instructors = db.relationship('Instructor', back_populates='users', cascade= 'all, delete', uselist= False)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'dive_level', 'is_admin', 'password')
        ordered = True