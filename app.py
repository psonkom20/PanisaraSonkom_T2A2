from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
# set string to connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://scuba_dev:spam123@127.0.0.1:5432/scuba_dive_shop'
# create new instance; connects everything together and return a db object
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70))
    contact_number = db.Column(db.Integer)
    dive_level = db.Column(db.String)
    DoB = db.Column(db.Date)

#create table in psql database
#Define a custom CLI (terminal) command
@app.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")



@app.route('/')
def index():
    return "Hello, world!"