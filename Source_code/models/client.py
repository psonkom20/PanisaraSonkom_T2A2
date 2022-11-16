from init import db, ma

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    users = db.relationship('User', back_populates='clients')
    bookings = db.relationship('Booking', back_populates='clients', cascade= 'all, delete')

class ClientSchema(ma.Schema):
    fields = ('id', 'user_id')
    ordered= True

