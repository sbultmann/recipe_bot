from flask import render_template, flash, redirect, url_for
from app import app, db
from app.functions import get_recipe, get_image, extract_recipe, extract_html
from app.forms import RecipeForm, ImportForm
from app.models import Recipe, Instructions, Ingredients



@app.route('/',methods=['GET', 'POST'])
def index():
    form = RecipeForm()
    if form.validate_on_submit():
        print("asking ChatGPT for help ...")
        recipe_data = get_recipe(form.dish_type.data, form.ingredients.data,form.recipe_type.data)
        print("asking DALL_E for help ...")
        print(recipe_data['prompt'])
        image = get_image(recipe_data['prompt'])
        print('storing info in database ...')

        #create a new recipe
        recipe = Recipe(title=recipe_data['title'],
                        image_id=image,
                        vegetarian = form.recipe_type.data,
                        dish_type = form.dish_type.data
                        )
        db.session.add(recipe)

        #create new ingredients
        for ingredient in recipe_data['ingredients']:
            new_ingredient = Ingredients(name=ingredient['name'], 
                                        unit=ingredient['unit'],
                                        amount=ingredient['amount'],
                                        recipe=recipe)
            db.session.add(new_ingredient)
        
        #create new instructions
        for instruction in recipe_data['instructions']:
            new_instruction = Instructions(instruction=instruction,
                                           recipe=recipe)
            db.session.add(new_instruction)

        db.session.commit()
        
        return redirect(f'/recipe/{recipe.id}')
    recipes = Recipe.query.all()
    return render_template('submit.html', title='Recipe Bot', form=form, recipes = recipes)

@app.route('/recipe/<id>')
def recipe(id):
    recipe = Recipe.query.filter_by(id=id).first_or_404()
    ingredients = []
    for ingredient in recipe.ingredients:
        if ingredient.amount.is_integer():
            amount = int(ingredient.amount)
        else:
            amount = ingredient.amount
        ingredients.append({'name':ingredient.name, 'unit':ingredient.unit, 'amount': amount})
    instructions = []
    for instruction in recipe.instructions:
         instructions.append(instruction.instruction)
    recipe_data = {
         'title':recipe.title,
         'ingredients':ingredients,
         'instructions':instructions
    }
    return render_template('recipe.html', title='Recipe Bot', recipe=recipe_data, image = recipe.image_id)

@app.route('/import_recipe',methods=['GET', 'POST'])
def import_recipe():
    form = ImportForm()
    if form.validate_on_submit():
        html = extract_html(form.url.data)
        recipe_data = extract_recipe(html)
        print("asking DALL_E for help ...")
        print(recipe_data['prompt'])
        image = get_image(recipe_data['prompt'])
        print('storing info in database ...')

        #create a new recipe
        recipe = Recipe(title=recipe_data['title'],
                        image_id=image,
                        dish_type = "imported"
                        )
        db.session.add(recipe)

        #create new ingredients
        for ingredient in recipe_data['ingredients']:
            new_ingredient = Ingredients(name=ingredient['name'], 
                                        unit=ingredient['unit'],
                                        amount=ingredient['amount'],
                                        recipe=recipe)
            db.session.add(new_ingredient)
        
        #create new instructions
        for instruction in recipe_data['instructions']:
            new_instruction = Instructions(instruction=instruction,
                                           recipe=recipe)
            db.session.add(new_instruction)

        db.session.commit()
        
        return redirect(f'/recipe/{recipe.id}')
    recipes = Recipe.query.all()
    return render_template('import.html', title='Recipe Bot', form=form, recipes = recipes)

@app.route('/kindle',methods=['GET', 'POST'])
def kindle_index():
    form = RecipeForm()
    if form.validate_on_submit():
        print("asking ChatGPT for help ...")
        recipe_data = get_recipe(form.dish_type.data, form.ingredients.data,form.recipe_type.data)
        print("asking DALL_E for help ...")
        print(recipe_data['prompt'])
        image = get_image(recipe_data['prompt'])
        print('storing info in database ...')

        #create a new recipe
        recipe = Recipe(title=recipe_data['title'],
                        image_id=image,
                        vegetarian = form.recipe_type.data,
                        dish_type = form.dish_type.data
                        )
        db.session.add(recipe)

        #create new ingredients
        for ingredient in recipe_data['ingredients']:
            new_ingredient = Ingredients(name=ingredient['name'], 
                                        unit=ingredient['unit'],
                                        amount=ingredient['amount'],
                                        recipe=recipe)
            db.session.add(new_ingredient)
        
        #create new instructions
        for instruction in recipe_data['instructions']:
            new_instruction = Instructions(instruction=instruction,
                                           recipe=recipe)
            db.session.add(new_instruction)

        db.session.commit()
        
        return redirect(f'/recipe/{recipe.id}')
    recipes = Recipe.query.all()
    return render_template('kindle_submit.html', title='Recipe Bot', form=form, recipes = recipes)

@app.route('/recipe_kindle/<id>')
def recipe_kindle(id):
    recipe = Recipe.query.filter_by(id=id).first_or_404()
    ingredients = []
    for ingredient in recipe.ingredients:
        if ingredient.amount.is_integer():
            amount = int(ingredient.amount)
        else:
            amount = ingredient.amount
        ingredients.append({'name':ingredient.name, 'unit':ingredient.unit, 'amount': amount})
    instructions = []
    for instruction in recipe.instructions:
         instructions.append(instruction.instruction)
    recipe_data = {
         'title':recipe.title,
         'ingredients':ingredients,
         'instructions':instructions
    }
    return render_template('kindle_recipe.html', title='Recipe Bot', recipe=recipe_data, image = recipe.image_id)