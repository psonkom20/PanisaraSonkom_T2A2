from flask import Blueprint, request
from init import db, bcrypt
from datetime import timedelta
from models.user import User, UserSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register/', methods=['POST'])
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

@auth_bp.route('/login/', methods = ['POST'])
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


