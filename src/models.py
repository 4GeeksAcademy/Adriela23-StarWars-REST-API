from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship("Favorites", backref = "user", uselist = True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    diameter = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    population = db.Column(db.String(15))
    terrain = db.Column(db.String(50))
    surface_water = db.Column(db.Integer)
    climate = db.Column(db.String(50))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "ratation_period": self.rotation_period,
            "population": self.population,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "climate": self.climate
        }


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.String(20))
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    gender = db.Column(db.String(20))

    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship("Planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "height": self.height,
            "mass": self.mass,
            "gender": self.gender,
            "planet_id": self.planet_id
        }
    


class Favorites(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column (db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    __table_args__= (db.UniqueConstraint(
        'user_id',
        'name',
        name= 'favorite_unique'
    ),)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id
        }
    
    @classmethod
    def create(cls, favorite):
        try:
            new_fav= cls(**favorite)
            db.session.add(new_fav)
            db.session.commit()
            return new_fav
        except Exception as error:
            print(error)
            db.session.rollback()
            return None
        

    @classmethod
    def delete(cls, favorite):
        try:
            db.session.delete(favorite)
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()
            return None
