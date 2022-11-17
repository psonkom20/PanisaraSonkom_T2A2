from flask import Blueprint, request
from init import db
from models.user import User, UserSchema
from controllers.auth_controller import authorize
from flask_jwt_extended import jwt_required


users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/')
# decode the token to see token is verify and that it is not expired
def get_all_users():
# Get all userss
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude= ['password']).dump(users)

@users_bp.route('/<int:id>/')
def get_one_users(id):
# Get one user by id number
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        return UserSchema(exclude= ['password']).dump(user)
    else:
        return {'error': f'User not found with id {id}'}, 404

@users_bp.route('/<string:dive_level>/')
def get_users_dive_level(dive_level):
# Get one user by dive level
    stmt = db.select(User).filter_by(dive_level=dive_level)
    users = db.session.scalar(stmt)
    if users:
        return UserSchema(exclude= ['password']).dump(users)
    else:
        return {'error': f'User not found with dive_level {dive_level}'}, 404

@users_bp.route('/<int:id>/', methods= ['DELETE'])
@jwt_required()
def delete_one_user(id):
# Delete a user by id
    authorize()

    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'message': f"User '{user.id}' deleted successfully"}
    else:
        return {'error': f'User not found with id {id}'}, 404

@users_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_user(id):
# Update a diver's dive lvl information
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:

        user.dive_lvl= request.json.get('dive_lvl') or user.dive_lvl

        db.session.commit()
        return UserSchema().dump(user)
    else:
        return {'error': f'User not found with id {id}'}, 404




