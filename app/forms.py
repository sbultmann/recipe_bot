from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class RecipeForm(FlaskForm):
    dish_type = SelectField('Dish Type', choices=[('main dish', 'Main dish'), ('side dish', 'Side dish'), ('desert', 'Desert')],validators=[DataRequired()])
    ingredients = StringField('Ingredients', validators=[DataRequired()])
    recipe_type = BooleanField('Make it veggie!')
    submit = SubmitField('Generate Recipe!')