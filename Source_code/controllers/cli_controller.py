from flask import Blueprint
from init import db, bcrypt
from datetime import date, datetime
from models.dive_trip import DiveTrip
from models.user import User
from models.client import Client
from models.instructor import Instructor
from models.booking import Booking


db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")


@db_commands.cli.command('seed')
def seed_db():
    users = [
    User(
        name = 'Jina Sonkom',
        email = 'jina@spam.com',
        password =bcrypt.generate_password_hash('spam456').decode('utf-8'),
        dive_level = 'Advanced open water diver',
        is_admin = True
    ),
    User(
        name = 'Jiji Sonkom',
        email = 'jiji@spam.com',
        password = bcrypt.generate_password_hash('egg123').decode('utf-8'),
        dive_level = 'Open water diver',
        is_admin = False
    ),
    User(
        name = 'Jan Wachi',
        email = 'jan@spam.com',
        password = 'cherry123',
        dive_level = 'Advanced open water diver',
        is_admin = False
    ),
    User(
        name = 'Kaitlyn Tiv',
        email = 'Kaitlyn@spam.com',
        password ='bread123',
        dive_level = 'Open water diver',
        is_admin = False
    ),
    User(
        name = 'Maggie Simpson',
        email = 'maggie@spam.com',
        password = bcrypt.generate_password_hash('bacon123').decode('utf-8'),
        dive_level = 'Dive Master',
        is_admin = False
    ),
    User(
        name = 'Peter Griffin',
        email = 'Peter@spam.com',
        password = bcrypt.generate_password_hash('bagel123').decode('utf-8'),
        dive_level = 'Dive Master',
        is_admin = False
    ),
    User(
        name = 'Rick Morty',
        email = 'rick@spam.com',
        password = bcrypt.generate_password_hash('pickle123').decode('utf-8'),
        dive_level = 'Dive Master',
        is_admin = False
    )
    ]
    db.session.add_all(users)
    db.session.commit()

    clients = [
        Client(
            user_id = users[1].id
        ),
        Client(
            user_id = users[2].id
        ),
        Client(
            user_id = users[3].id
        )
    ]
    db.session.add_all(clients)
    db.session.commit()

    instructors = [
        Instructor(
            user_id = users[4].id
        ),
        Instructor(
            user_id = users[5].id
        ),
        Instructor(
            user_id = users[6].id
        )
    ]
    db.session.add_all(instructors)
    db.session.commit()

    dive_trips = [
        DiveTrip(
            name = 'Sail Rock Dive Trip',
            dive_lvl_required = 'Advanced open water diver',
            location = 'Sail Rock, Koh Tao',
            date = 'November 25, 2022',
            max_no_people = 6,
            description= 'lorem ipsum dolor sit amet, consectetur adipiscing',
            instructor_id = instructors[0].id
        ),
        DiveTrip(
            name='Japanese Garden Dive Trip',
            dive_lvl_required = 'Open water diver',
            location = 'Japanese Garden, Koh Tao',
            date = 'November 25, 2022',
            max_no_people = 8,
            description= 'lorem ipsum dolor sit amet, consectetur adipiscing',
            instructor_id = instructors[1].id
        ),
        DiveTrip(
            name = 'Junk Yard Dive Trip',
            dive_lvl_required = 'Advanced open water diver',
            location = 'Junk Yard, Koh Tao',
            date = 'November 25, 2022',
            max_no_people = 5,
            description= 'lorem ipsum dolor sit amet, consectetur adipiscing',
            instructor_id = instructors[1].id
        ),
        DiveTrip(
            name = 'Manly Cove Dive Trip',
            dive_lvl_required = 'Advanced open water diver',
            location = 'Manly Cove, Manly',
            date = 'November 25, 2022',
            max_no_people = 4,
            description= 'lorem ipsum dolor sit amet, consectetur adipiscing',
            instructor_id = instructors[2].id
        ),
        DiveTrip(
            name = 'Fairy Bower Dive Trip',
            dive_lvl_required = 'Open water diver',
            location = 'Fairy Bower, Manly',
            date = 'November 25, 2022',
            max_no_people = 5,
            description= 'lorem ipsum dolor sit amet, consectetur adipiscing',
            instructor_id = instructors[2].id
        )
    ]
    db.session.add_all(dive_trips)
    db.session.commit()

    bookings = [
        Booking(
            date = date.today(),
            time = datetime.now(),
            dive_trip_id = dive_trips[1].id,
            client_id = clients[0].id
        ),
        Booking(
            date = date.today(),
            time = datetime.now(),
            dive_trip_id = dive_trips[3].id,
            client_id = clients[1].id
        ),
        Booking(
            date = date.today(),
            time = datetime.now(),
            dive_trip_id = dive_trips[4].id,
            client_id = clients[2].id
        )
    ]
    db.session.add_all(bookings)
    db.session.commit()

    print('Tables seeded')
