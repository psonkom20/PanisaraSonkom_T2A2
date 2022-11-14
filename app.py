from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

app= Flask(__name__)
app.config ['JSON_SORT_KEYS'] = False
# set string to connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://scuba_dev:spam123@127.0.0.1:5432/scuba_dive_shop'
# create new instance; connects everything together and return a db object
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)

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

# give marshmallow info in needs to convert user instances to json
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'contact_number', 'dive_level', 'DoB', 'is_admin')
        ordered = True

#create table in psql database
#Define a custom CLI (terminal) command
@app.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")

@app.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")


@app.cli.command('seed')
def seed_db():
    users = [
    User(
        name = 'Jina Sonkom',
        email = 'jina@spam.com',
        password =bcrypt.generate_password_hash('spam123').decode('utf-8'),
        contact_number = '0819877825',
        dive_level = 'Advanced open water diver',
        DoB = date(1999, 4, 20),
        is_admin = True
    ),
    User(
        name = 'Jiji Sonkom',
        email = 'jiji@spam.com',
        password = bcrypt.generate_password_hash('egg123').decode('utf-8'),
        contact_number = '0819877826',
        dive_level = 'Open water diver',
        DoB = date(1997, 11, 11),
        is_admin = False
    ),
    User(
        name = 'Jan Wachi',
        email = 'jan@spam.com',
        password = 'cherry123',
        contact_number = '0819877827',
        dive_level = 'Advanced open water diver',
        DoB = date(1999, 9, 20),
        is_admin = False
    ),
    User(
        name = 'Kaitlyn Tiv',
        email = 'Kaitlyn@spam.com',
        password ='bread123',
        contact_number = '0819877828',
        dive_level = 'Open water diver',
        DoB = date(1996, 5, 20),
        is_admin = False
    )
    ]
# use 'add' when adding singular card; use add_all from multiple
    db.session.add_all(users)
    db.session.commit()
    print('Tables seeded')
#change from cli commant to route and change parameter to route format add return CardSchema().dump(), import marshmallow to serialize return
@app.route('/users/')
def all_users():
    #function :select * from users;
    # use db.session.execute(stmt).all() to select specific columns/field. unident code below
        #stmt = db.select(User.name, User.dive_level)
        #users = db.session.execute(stmt).all()
    #To get users that have specific attribute
        # user 'db.or_' to select condition. Have this attribute or this attribute
    #stmt = db.select(User).where(db.or_(User.dive_level == 'Advanced open water diver', User.name == 'Jiji Sonkom'))
    # when using filter_by do not need User.dive_leve; singular '='
    #stmt = db.select(User).filter_by(dive_level = 'Open water diver')
    #stmt = db.select(User).order_by(User.DoB.desc())
    stmt = db.select(User).filter_by(is_admin = True)
    users = db.session.scalars(stmt)
    return UserSchema(many=True).dump(users)
    #for user in users:
    #    print(user.DoB)
    #print(users)
    #print(users[0].__dict__)

@app.cli.command('first_user')
def first_user():
    #select * from users, limit 1;
    #singular 'scalar' cos returning one user
    stmt = db.select(User).limit(1)
    user = db.session.scalar(stmt)
    print(user.__dict__)
#.all() print answer in desired result use .one() for answer with no list format or scalar instead of scalars (if one result use scalar, if multiple results use scalars cos always in list format)
#count user(object)
@app.cli.command('count_users')
def count_users():
    stmt = db.select(db.func.count()).select_from(User)
    users= db.session.scalar(stmt)
    print(users)

@app.route('/')
def index():
    return "Hello, world!"