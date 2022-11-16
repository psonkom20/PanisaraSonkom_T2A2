from flask import Blueprint
from db import db
from models.dive_trip import DiveTrip, DiveTripSchema

dive_trips_bp = Blueprint('dive_trips', __name__, url_prefix='/dive_trips')

@dive_trips_bp.route('/')
# decode the token to see token is verify and that it is not expired
#@jwt_required()
def all_dive_trips():

    #if not authorize():
    #    return {'error': 'You must be an admin'}, 401
    stmt = db.select(DiveTrip)
    dive_trips = db.session.scalars(stmt)
    return DiveTripSchema(many=True).dump(dive_trips)

@dive_trips_bp.route('/<int:id>/')
# select one card by id number
def one_card(id):
    stmt = db.select(DiveTrip).filter_by(id=id)
    dive_trip = db.session.scalar(stmt)
    return DiveTripSchema().dump(dive_trip)