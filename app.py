from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager,create_access_token, jwt_required

app= Flask(__name__)

app.config ['JSON_SORT_KEYS'] = False
# set string to connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://scuba_dev:spam123@127.0.0.1:5432/scuba_dive_shop'
app.config['JWT_SECRET_KEY'] = 'hello there'
# create new instance; connects everything together and return a db object
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

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
        fields = ('id', 'name', 'email', 'contact_number', 'dive_level', 'DoB', 'is_admin', 'password')
        ordered = True


class DiveTrip(db.Model):
    __tablename__ = 'dive_trips'
    id= db.Column(db.Integer, primary_key=True)
    dive_lvl_required=db.Column(db.String, nullable = False)
    location= db.Column(db.String, nullable = False)
    date= db.Column(db.Date, nullable = False)
    description= db.Column(db.String, nullable = False)
    max_no_people=db.Column(db.Integer, nullable = False)
    # add instructor ID

class DiveTripSchema(ma.Schema):
    class Meta:
        fields = ('id', 'dive_lvl_required', 'location', 'date', 'description', 'max_no_people')
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
        password =bcrypt.generate_password_hash('spam456').decode('utf-8'),
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
    dive_trips = [
        DiveTrip(
            dive_lvl_required = 'Advanced open water diver',
            location = 'Sail Rock, Koh Tao',
            date = date(2022,12,5),
            max_no_people = 6,
            description= 'lorem ipsum dolor sit amet, consectetur adipiscing'
        ),
        DiveTrip(
            dive_lvl_required = 'Open water diver',
            location = 'Japanese Garden, Koh Tao',
            date = date(2022,11,24),
            max_no_people = 8,
            description= 'lorem ipsum dolor sit amet, consectetur adipiscing'
        ),
        DiveTrip(
            dive_lvl_required = 'Advanced open water diver',
            location = 'Junk Yard, Koh Tao',
            date = date(2022,12,25),
            max_no_people ='6',
            description= 'lorem ipsum dolor sit amet, consectetur adipiscing'
        )
    ]
# use 'add' when adding singular card; use add_all from multiple
    db.session.add_all(users)
    db.session.add_all(dive_trips)
    db.session.commit()
    print('Tables seeded')

@app.route('/auth/register/', methods=['POST'])
def auth_register():
    try:
        # Load the posted user info and parse the JSON
        user_info = UserSchema().load(request.json)
        # Create a new User model instance from the user_info
        user = User(
            email= request.json['email'],
            password=bcrypt.generate_password_hash(request.json['password']).decode('utf-8'),
            name=request.json['name'],
            dive_level=request.json['dive_level'],

        )
        # Add and commit user to DB
        db.session.add(user)
        db.session.commit()
        # Respond to client
        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {'error': 'Email address already registered'}, 409

@app.route('/auth/login/', methods = ['POST'])
def auth_login():
    # Find a user by email address
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)
    # If user exist and password is correct
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        #return UserSchema(exclude=['password']).dump(user)
        token = create_access_token(identity=str(user.id),expires_delta=timedelta(days=1))
        return {'email': user.email, 'token': token, 'is_admin': user.is_admin}
    else:
        return {'error': 'Invalid email or password'}, 401

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
@app.route('/dive_trips/')
# decode the token to see token is verify and that it is not expired
@jwt_required()
def all_dive_trips():
    stmt = db.select(DiveTrip)
    dive_trips = db.session.scalars(stmt)
    return DiveTripSchema(many=True).dump(dive_trips)

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