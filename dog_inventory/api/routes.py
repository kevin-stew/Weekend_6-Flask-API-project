from flask import Blueprint, jsonify, request
from flask_login import login_required
from dog_inventory.helpers import token_required
from dog_inventory.models import db, User, Dog, dog_schema, dogs_schema

api = Blueprint('api',__name__, url_prefix = '/api')

@api.route('getdata')
@token_required
def getdata(current_user_token):
    return jsonify({'some':'value',
                    'Other':44.3})

# Create Dog Route
@api.route('/dogs', methods=['POST'])
@token_required
def create_dog(current_user_token):
    name = request.json['name']
    description = request.json['description']
    competitions_attended = request.json['competitions_attended']
    notable_quality = request.json['notable_quality']
    date_created = request.json['date_created']
    user_token = current_user_token.token


    dog = Dog(name, description, competitions_attended, notable_quality, date_created, user_token)
    db.session.add(dog)

    db.session.commit()

    response = dog_schema.dump(dog)
    return jsonify(response)

# Retrieve ALL dogs
@api.route('/dogs', methods=['GET'])
@token_required
def get_dogs(current_user_token):
    owner = current_user_token.token
    dogs = Dog.query.filter_by(user_token = owner).all()
    response = dogs_schema.dump(dogs)
    return jsonify(response)

# Retrieve a dog
@api.route('/dogs/<id>', methods=['GET'])
@token_required
def get_dog(current_user_token,id):
    owner = current_user_token.token  # might be an issue
    dog = Dog.query.get(id)
    response = dog_schema.dump(dog)
    return jsonify(response)

# UPDATE a dog
@api.route('/dogs/<id>', methods=['POST','PUT'])
@token_required
def update_dog(current_user_token, id):
    dog = Dog.query.get(id)

    dog.name = request.json['name']
    dog.description = request.json['description']
    dog.competitions_attended = request.json['competitions_attended']
    dog.notable_quality = request.json['notable_quality']
    dog.date_created = request.json['date_created']
    
    db.session.commit()
    response = dog_schema.dump(dog)
    return jsonify(response)

# DELETE a dog
@api.route('/dogs/<id>', methods = ['DELETE'])
@token_required
def delete_dog(current_user_token, id):
    dog = Dog.query.get(id)
    db.session.delete(dog)
    db.session.commit()

    response = dog_schema.dump(dog)
    return jsonify(response)