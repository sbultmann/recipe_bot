from flask import render_template, flash, redirect, url_for
from app import app
from app.functions import get_recipe, get_image
from app.forms import RecipeForm


@app.route('/',methods=['GET', 'POST'])
def index():
    form = RecipeForm()
    if form.validate_on_submit():
        if form.recipe_type.data:
            recipe_type = 'vegetarian'
        else: 
            recipe_type = ''
        print("asking ChatGPT for help ...")
        recipe = get_recipe(form.dish_type.data, form.ingredients.data,recipe_type)
        print("asking DALL_E for help ...")
        image = get_image(recipe['title'])
        
        return render_template('recipe.html', title='Recipe Bot', form=form, recipe=recipe, image = image)
    return render_template('submit.html', title='Recipe Bot', form=form)

@app.route('/recipe')
def recipe():
    
    return render_template('base.html', title='Recipe Bot')
