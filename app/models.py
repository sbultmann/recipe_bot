from datetime import datetime
from app import db

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    image_id = db.Column(db.String(64))
    vegetarian = db.Column(db.Boolean())
    dish_type = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    ingredients = db.relationship('Ingredients', backref='recipe', lazy='dynamic')
    instructions = db.relationship('Instructions', backref='recipe', lazy='dynamic')
    def __repr__(self):
        return f'<Recipe: {self.title}>'

class Ingredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    unit = db.Column(db.String(140))
    amount = db.Column(db.Float())
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    def __repr__(self):
        return f'<Ingredient: {self.name}>'
    
class Instructions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instruction = db.Column(db.String(140))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    def __repr__(self):
        return f'<Instructions: {self.recipe_id}>'