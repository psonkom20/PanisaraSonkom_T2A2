from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
# set string to connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://scuba_dev:spam123@127.0.0.1:5432/scuba_dive_shop'
# create new instance; connects everything together and return a db object
db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Hello, world!"