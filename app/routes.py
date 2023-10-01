from flask import render_template, redirect, url_for, request
from app import app, db
from app.functions import get_recipe, get_image, extract_from_website, save_recipe, save_image, image_to_text
from app.forms import RecipeForm, ImportForm, ImportTextForm, UploadForm
from app.models import Recipe, Instructions, Ingredients
from app.ai_config import we_chain


@app.route('/',methods=['GET', 'POST'])
def index():
    recipes = Recipe.query.all()
    imported = []
    main = []
    side = []
    desert = []
    for recipe in recipes:
        #print(recipe.dish_type)
        if recipe.dish_type == 'Hauptgericht':
            main.append(recipe)
        elif recipe.dish_type == 'Beilage':
            side.append(recipe)
        elif recipe.dish_type == 'Nachtisch':
            desert.append(recipe)
        elif recipe.dish_type == 'imported':
            imported.append(recipe)

    return render_template('index.html', title='Recipe Bot', imported = imported, main = main, side = side, desert = desert)


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
    recipe['ingredients'] = [{'amount':int(ingredient['amount']), 'unit':ingredient['unit'], 'name': ingredient['name']} if ingredient['amount'].is_integer()
                             else {'amount':ingredient['amount'], 'unit':ingredient['unit'], 'name': ingredient['name']}
                             for ingredient in recipe['ingredients'] ]
    return render_template('recipe.html', title='Recipe Bot', recipe=recipe, image = recipe['image_id'])

@app.route('/delete/<id>')
def delete(id):
    #Recipe.query.filter_by(id=id).delete()
    recipe = db.session.query(Recipe).filter(Recipe.id==id).first()
    db.session.delete(recipe)
    db.session.commit()
    recipes = Recipe.query.all()
    imported = []
    main = []
    side = []
    desert = []
    for recipe in recipes:
        #print(recipe.dish_type)
        if recipe.dish_type == 'Hauptgericht':
            main.append(recipe)
        elif recipe.dish_type == 'Beilage':
            side.append(recipe)
        elif recipe.dish_type == 'Nachtisch':
            desert.append(recipe)
        elif recipe.dish_type == 'imported':
            imported.append(recipe)
    return render_template('index.html', title='Recipe Bot', imported = imported, main = main, side = side, desert = desert)

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

@app.route('/recipe_kindle/<id>')
def recipe_kindle(id):
    recipe = Recipe.query.filter_by(id=id).first_or_404()
    recipe = recipe.to_dict()
    return render_template('kindle_recipe.html', title='Recipe Bot', recipe=recipe)