from main import db, ma

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="clients")

class ClientSchema(ma.Schema):
    fields = ('id', 'user_id')
    ordered= True

