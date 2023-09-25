from datetime import datetime
from app import db
from sqlalchemy_serializer import SerializerMixin



class Recipe(db.Model, SerializerMixin):

    serialize_rules = ('-ingredients.recipe','-instructions.recipe','-naehrwerte.recipe')
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    prompt = db.Column(db.Text)
    beschreibung = db.Column(db.Text)
    portionen = db.Column(db.Integer)
    recipe_type = db.Column(db.String(64))
    image_id = db.Column(db.String(64))
    dish_type = db.Column(db.String(64))
    recipe_type = db.Column(db.String(64))
    tipp = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    ingredients = db.relationship('Ingredients', backref='recipe', lazy='dynamic')
    instructions = db.relationship('Instructions', backref='recipe', lazy='dynamic')
    naehrwerte = db.relationship('Naehrwerte', backref='recipe', lazy='dynamic')
    def __repr__(self):
        return f'<Recipe: {self.title}>'

class Ingredients(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    unit = db.Column(db.String(140))
    amount = db.Column(db.Float())
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    def __repr__(self):
        return f'<Ingredient: {self.name}>'

class Naehrwerte(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    unit = db.Column(db.String(140))
    amount = db.Column(db.Float())
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    def __repr__(self):
        return f'<Naehrwert: {self.name}>'
    
class Instructions(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    instruction = db.Column(db.Text)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    def __repr__(self):
        return f'<Instructions: {self.recipe_id}>'