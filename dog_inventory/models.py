import uuid
from datetime import datetime
import secrets

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow

from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# user model creation
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(50), nullable = True, default = '')
    email_name = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    token = db.Column(db.String, default='', unique = True)   # single to one relationship (one user can have many dogs)
    g_auth_verify = db.Column(db.Boolean, default = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    dog = db.relationship('Dog', backref = 'owner', lazy = True) # helper code that user_token is FK with dog 


    def __init__(self, email, name = '', id='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.name = name
        self.password = self.set_password(password)
        self.email_name = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)


    def __repr__(self):
        return f'User {self.email_name} has been added to the database.'

# Dog model creation
class Dog(db.Model):
    id = db.Column(db.String(50), primary_key = True)
    name = db.Column(db.String(50), nullable = True, default = '')
    description = db.Column(db.String(200), nullable = True)
    competitions_attended = db.Column(db.Numeric(precision=100, scale=0))
    notable_quality = db.Column(db.String(200), nullable = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)  # many to one relationship (many dogs can be assigend to one user)
    # camera_quality = db.Column(db.String(50), nullable = True)
    # flight_time = db.Column(db.String(100))
    # max_speed = db.Column(db.String(100))
    # dimensions = db.Column(db.String(100))
    # weight = db.Column(db.String(50))
    # cost_of_production = db.Column(db.Numeric(precision=10, scale=2))
    # series = db.Column(db.String(100))

    def __init__(self, name, description, competitions_attended, notable_quality, date_created, user_token, id=''): 
                    #price, camera_quality, flight_time, max_speed, dimensions, weight, cost_of_production, series, user_token, id='')
    
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.competitions_attended = competitions_attended
        self.notable_quality = notable_quality
        self.date_created = date_created
        self.user_token = user_token
        # self.price = price
        # self.camera_quality = camera_quality
        # self.flight_time = flight_time
        # self.max_speed = max_speed
        # self.dimensions = dimensions
        # self.weight = weight
        # self.cost_of_production = cost_of_production
        # self.series = series

    def set_id(self):
        return secrets.token_urlsafe()

    def __repr__(self):
        return f"The following dog has been entered/created: {self.name}"


# Creation of API Schema via the Marshmallow Object
class DogSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'competitions_attended', 'notable_quality', 'date_created']  #date_created might give an error

#'price', 'camera_quality', 'flight_time', 'max_speed', 'dimensions', 'weight', 'cost_of_production', 'series']

dog_schema = DogSchema()
dogs_schema = DogSchema(many=True)