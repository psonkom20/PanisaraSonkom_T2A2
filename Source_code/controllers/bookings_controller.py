from flask import Blueprint, request
from init import db
from models.booking import Booking, BookingSchema
from models.dive_trip import DiveTrip, DiveTripSchema
from models.user import User, UserSchema
from controllers.auth_controller import authorize
from flask_jwt_extended import jwt_required, get_jwt_identity


bookings_bp = Blueprint('bookings', __name__, url_prefix='/bookings')

@bookings_bp.route('/')
def get_all_bookings():
# Get all bookings
    stmt = db.select(Booking)
    booking = db.session.scalars(stmt)
    return BookingSchema(many=True).dump(booking)

@bookings_bp.route('/<int:id>/')
def get_one_booking(id):
# Get one booking by id number
    stmt = db.select(Booking).filter_by(id=id)
    booking = db.session.scalar(stmt)
    if booking:
        return BookingSchema().dump(booking)
    else:
        return {'error': f'Booking not found with id {id}'}, 404

@bookings_bp.route('/<int:id>/', methods= ['DELETE'])
@jwt_required()
def delete_one_booking(id):
# Delete a booking by id number
    authorize()

    stmt = db.select(Booking).filter_by(id=id)
    booking = db.session.scalar(stmt)
    if booking:
        db.session.delete(booking)
        db.session.commit()
        return {'message': f"Booking '{booking.id}' deleted successfully"}
    else:
        return {'error': f'Booking not found with id {id}'}, 404

@bookings_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_booking(id):
# Update a booking's information
    stmt = db.select(Booking).filter_by(id=id)
    booking = db.session.scalar(stmt)
    if booking:

        booking.dive_trip_id= request.json.get('dive_trip_id') or booking.dive_trip_id

        db.session.commit()
        return BookingSchema().dump(booking)
    else:
        return {'error': f'Booking not found with id {id}'}, 404


@bookings_bp.route('/', methods=['POST'])
def create_booking():
    data = BookingSchema().load(request.json, partial = True)
    # Create a new booking model instance
    booking = Booking(

        dive_trip_id= data['dive_trip_id'],
        user_id = data['user_id'],


    )
    # Add and commit bookings to DB
    db.session.add(booking)
    db.session.commit()
    # Respond to client
    return BookingSchema().dump(booking), 201

