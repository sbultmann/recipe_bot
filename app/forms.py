from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField, TextAreaField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, Length

class RecipeForm(FlaskForm):
    dish_type = SelectField('Art', choices=[('Hauptgericht', 'Hauptgericht'), ('Beilage', 'Beilage'), ('Nachtisch', 'Nachtisch')],validators=[DataRequired()])
    ingredients = StringField('Zutaten', validators=[DataRequired()])
    recipe_type = BooleanField('Make it veggie!')
    submit = SubmitField("Rezept erzeugen!")

class ImportForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired()])
    submit = SubmitField('Import Recipe!')

class ImportTextForm(FlaskForm):
    text = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('Import Recipe!')

class UploadForm(FlaskForm):
    file = FileField('Image')
    submit = SubmitField("Upload")