from flask import render_template, redirect, url_for, request
from app import app, db
from app.functions import get_recipe, get_image, extract_from_website, save_recipe, save_image, image_to_text
from app.forms import RecipeForm, ImportForm, ImportTextForm, UploadForm
from app.models import Recipe, Instructions, Ingredients
from app.ai_config import we_chain


@app.route('/',methods=['GET', 'POST'])
def index():
    recipes = Recipe.query.all()
    return render_template('collection.html', title='Recipe Bot', recipes = recipes)


@app.route('/generate',methods=['GET', 'POST'])
def generate():
    form = RecipeForm()
    return render_template('submit.html', title='Recipe Bot', form=form)

@app.route('/generate_recipe',methods=['GET', 'POST'])
def generate_recipe():
    print(request.form)
    try:
        recipe_type = request.form['recipe_type']
    except:
        recipe_type = ''
    recipe_data = get_recipe(request.form['dish_type'], request.form['ingredients'],recipe_type)
    recipe_id = save_recipe(recipe_data, request.form['dish_type'])
    return url_for('recipe', id = recipe_id)


@app.route('/recipe/<id>')
def recipe(id):
    recipe = Recipe.query.filter_by(id=id).first_or_404()
    recipe = recipe.to_dict()
    return render_template('recipe.html', title='Recipe Bot', recipe=recipe, image = recipe['image_id'])

@app.route('/import_recipe',methods=['GET', 'POST'])
def import_recipe():
    form = ImportForm()
    return render_template('import.html', title='Recipe Bot', form=form)

@app.route('/generate_from_web',methods=['GET', 'POST'])
def generate_from_web():
    html = extract_from_website(request.form['url'])
    recipe_data = we_chain.run(text=html).dict()
    recipe_id = save_recipe(recipe_data, "imported")
    return url_for('recipe', id = recipe_id)

@app.route('/import_from_image',methods=['GET', 'POST'])
def import_from_image():
    form = UploadForm()
    return render_template('import_from_image.html', title='Recipe Bot', form=form)

@app.route('/import_from_text',methods=['GET', 'POST'])
def import_from_text():
    form = ImportTextForm()
    if request.method == 'POST':
        path = save_image(request.files['file'])
        form.text.data = image_to_text(path)
    return render_template('import_from_text.html', title='Recipe Bot', form=form)

@app.route('/generate_from_text',methods=['GET', 'POST'])
def generate_from_text():
    recipe_data = we_chain.run(text=request.form['text']).dict()
    recipe_id = save_recipe(recipe_data, "imported")
    return url_for('recipe', id = recipe_id)

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