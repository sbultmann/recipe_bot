from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length

class RecipeForm(FlaskForm):
    dish_type = SelectField('Dish Type', choices=[('main dish', 'Main dish'), ('side dish', 'Side dish'), ('desert', 'Desert')],validators=[DataRequired()])
    ingredients = StringField('Ingredients', validators=[DataRequired()])
    recipe_type = BooleanField('Make it veggie!')
    submit = SubmitField('Generate Recipe!')

class ImportForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired()])
    submit = SubmitField('Import Recipe!')

class ImportTextForm(FlaskForm):
    text = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('Import Recipe!')