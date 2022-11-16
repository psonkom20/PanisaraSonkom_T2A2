from flask import Blueprint, request
from db import db
from models.dive_trip import DiveTrip, DiveTripSchema

dive_trips_bp = Blueprint('dive_trips', __name__, url_prefix='/dive_trips')

@dive_trips_bp.route('/')
# decode the token to see token is verify and that it is not expired
#@jwt_required()
def get_all_trips():
# Get all dive trips
    #if not authorize():
    #    return {'error': 'You must be an admin'}, 401
    stmt = db.select(DiveTrip)
    dive_trips = db.session.scalars(stmt)
    return DiveTripSchema(many=True).dump(dive_trips)

@dive_trips_bp.route('/<int:id>/')
def get_one_trip(id):
# Get one dive trip by id number
    stmt = db.select(DiveTrip).filter_by(id=id)
    dive_trip = db.session.scalar(stmt)
    if dive_trip:
        return DiveTripSchema().dump(dive_trip)
    else:
        return {'error': f'Trip not found with id {id}'}, 404

@dive_trips_bp.route('/<int:id>/', methods= ['DELETE'])
def delete_one_trip(id):
# Get one dive trip by id number
    stmt = db.select(DiveTrip).filter_by(id=id)
    dive_trip = db.session.scalar(stmt)
    if dive_trip:
        db.session.delete(dive_trip)
        db.session.commit()
        return {'message': f'Trip "{dive_trip.name}" deleted successfully'}
    else:
        return {'error': f'Trip not found with id {id}'}, 404

@dive_trips_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
def update_one_trip(id):
# Update a trip's information
    stmt = db.select(DiveTrip).filter_by(id=id)
    dive_trip = db.session.scalar(stmt)
    if dive_trip:

        dive_trip.dive_lvl_required= request.json.get('dive_lvl_required') or dive_trip.dive_lvl_required
        dive_trip.location=request.json.get('location') or dive_trip.location
        dive_trip.date= request.json.get('date') or dive_trip.date
        dive_trip.description=request.json.get('description') or dive_trip.description
        dive_trip.max_no_people= request.json.get('max_no_people') or dive_trip.max_no_people
        db.session.commit()
        return DiveTripSchema().dump(dive_trip)
    else:
        return {'error': f'Trip not found with id {id}'}, 404


@dive_trips_bp.route('/', methods=['POST'])
def create_card():
    # Create a new DiveTrip model instance
    dive_trip = DiveTrip(
        name= request.json['name'],
        dive_lvl_required= request.json['dive_lvl_required'],
        location=request.json['location'],
        date= request.json['date'],
        description=request.json['description'],
        max_no_people= request.json['max_no_people']
    )
    # Add and commit dive trips to DB
    db.session.add(dive_trip)
    db.session.commit()
    # Respond to client
    return DiveTripSchema().dump(dive_trip), 201

