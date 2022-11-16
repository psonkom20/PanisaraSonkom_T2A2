from main import db, ma

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), nullable = False, unique= True)
    password = db.Column(db.String, nullable = False)
    contact_number = db.Column(db.Integer)
    dive_level = db.Column(db.String)
    DoB = db.Column(db.Date)
    is_admin = db.Column(db.Boolean, default = False)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'contact_number', 'dive_level', 'DoB', 'is_admin', 'password')
        ordered = True