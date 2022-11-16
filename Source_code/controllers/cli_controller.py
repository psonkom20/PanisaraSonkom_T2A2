from flask import Blueprint
from init import db, bcrypt
from datetime import date
from models.dive_trip import DiveTrip
from models.user import User


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
    )
    ]
    dive_trips = [
        DiveTrip(
            name = 'Sail Rock Dive Trip',
            dive_lvl_required = 'Advanced open water diver',
            location = 'Sail Rock, Koh Tao',
            date = 'November 25, 2022',
            max_no_people = 6,
            description= 'lorem ipsum dolor sit amet, consectetur adipiscing'
        ),
        DiveTrip(
            name='Japanese Garden Dive Trip',
            dive_lvl_required = 'Open water diver',
            location = 'Japanese Garden, Koh Tao',
            date = 'November 25, 2022',
            max_no_people = 8,
            description= 'lorem ipsum dolor sit amet, consectetur adipiscing'
        ),
        DiveTrip(
            name = 'Junk Yard Dive Trip',
            dive_lvl_required = 'Advanced open water diver',
            location = 'Junk Yard, Koh Tao',
            date = 'November 25, 2022',
            max_no_people ='6',
            description= 'lorem ipsum dolor sit amet, consectetur adipiscing'
        )
    ]
# use 'add' when adding singular card; use add_all from multiple
    db.session.add_all(users)
    db.session.add_all(dive_trips)
    db.session.commit()
    print('Tables seeded')
