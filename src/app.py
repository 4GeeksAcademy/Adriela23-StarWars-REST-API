"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


# endpoint to GET users
@app.route('/user', methods=['GET'])
def get_user():

    users= User.query.all()
    response= list(map(lambda user: user.serialize(), users))

    return jsonify(response), 200


# endpoint to GET user favorites
@app.route('/user/favorite', methods=['GET'])
def get_user_favs():

    favorites= Favorite.query.all()
    response= list(map(lambda favorite: favorite.serialize(), favorites))

    return jsonify(response), 200


# endpoint to GET characters
@app.route('/character', methods=['GET'])
def get_character():
    characters= Character.query.all() # devuelve una lista y es una consulta

    response= list(map(lambda character: character.serialize(), characters))
    # response= [character.serialize() for character in characters]

    return jsonify(response), 200


# endpoint to GET character by id
@app.route('/character/<int:character_id>', methods=['GET'])
def get_character_byid(character_id):
    character= Character.query.get(character_id)

    if not character:
        raise APIException("Character not found", status_code= 404)
    return jsonify(character.serialize()), 200


# endpoint to GET planets
@app.route('/planet', methods=['GET'])
def get_planet():

    planet= Planet.query.all()
    response= list(map(lambda planet: planet.serialize(), planets))

    return jsonify(response), 200


# endpoint to GET planet by id
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_byid(planet_id):
    planet= Planet.query.get(planet_id)

    if not planet:
        raise APIException("Planet not found", status_code= 404)
    return jsonify(planet.serialize()), 200


# endpoint to POST favorite character
@app.route('/favorite/character/<int:character_id>', methods=['POST'])

def add_fav_character(character_id):
    current_user= 1
    character= Character.query.filter_by(id = character_id).first() #retorna el primer resultado de este query y en caso en caso contrario retorna none
    
    if character is not None:
        favorite= favorite.query.filter_by(name = character.name).first()

        if favorite:
            return jsonify({'ok': True, 'message': 'fav exists'}), 200
        body= {
                'name': character.name,
                'user_id': current_user
                }
        new_fav= Favorite.create(body)
        if new_fav is not None:
            return jsonify(new_fav.serialize()), 201
        
        return jsonify({'message': 'server error'}), 500
        
    return jsonify({'message': 'not found'}), 404

    # character= Character.query.filter_by(id = character_id).first()
    # if character is not None:
    #     favorite= favorite.query.filter_by(name = character.name).first()
    #     if favorite:
    #         return jsonify({'ok': True, 'message': 'fav exists'}), 200
    #     new_fav= Favorite(name = character.name, user_id = current_user)
    #     try:
    #         db.session.add(new_fav)
    #         db.session.commit()
    #         return jsonify(new_fav.serialize()), 201
    #     except Exception as error:
    #         db.session.rollback()
    #         return jsonify(error.args), 500
    # return jsonify({'message': 'not found'}), 404


# endpoint to POST favorite planet
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])

def add_fav_planet(planet_id):
    current_user= 1
    planet= Planet.query.filter_by(id = planet_id).first()
    
    if planet is not None:
        favorite= favorite.query.filter_by(name = planet.name).first()

        if favorite:
            return jsonify({'ok': True, 'message': 'fav exists'}), 200
        body= {
                'name': planet.name,
                'user_id': current_user
                }
        new_fav= Favorite.create(body)
        if new_fav is not None:
            return jsonify(new_fav.serialize()), 201
        
        return jsonify({'message': 'server error'}), 500
        
    return jsonify({'message': 'not found'}), 404


# endpoint to DELETE favorite character by id
@app.route("/favorite/character/<int:character_id>", methods=['DELETE'])
def delete_favorite_character(character_id):
    current_user = 1
    character = Character.query.filter_by(id=character_id).first()

    if character is not None:
        favorite = Favorite.query.filter_by(name=character.name, user_id=current_user).first()

        if not favorite:
            return jsonify({"ok": False, "message": "Favorite does not exist"}), 404

        try:
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({"ok": True, "message": "Favorite deleted"}), 200
        except Exception as error:
            print(error)
            db.session.rollback()
            return jsonify({"message": "Server error"}), 500
    return jsonify({
        "message": "Not found"
    }), 404


# endpoint to DELETE favorite planet by id
@app.route("/favorite/planet/<int:planet_id>", methods=['DELETE'])
def delete_favorite_planet(planet_id):
    current_user = 1
    planet = Planet.query.filter_by(id=planet_id).first()

    if planet is not None:
        favorite = Favorite.query.filter_by(name=planet.name, user_id=current_user).first()

        if not favorite:
            return jsonify({"ok": False, "message": "Favorite does not exist"}), 404

        try:
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({"ok": True, "message": "Favorite deleted"}), 200
        except Exception as error:
            print(error)
            db.session.rollback()
            return jsonify({"message": "Server error"}), 500
    return jsonify({
        "message": "Not found"
    }), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
