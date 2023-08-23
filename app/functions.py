
import openai
import json
from app import app
import urllib.request
import os

openai.api_key = app.config["OPENAI_API"]

#JSON output schema
schema = {
    "type": "object",
    "properties": {
    "title": {
        "type": "string",
        "description": "creative recipe title"
        },
    "ingredients": {
        "type": "array",
        "items": {
        "type": "object",
        "properties": {
            "name": { "type": "string" },
            "unit": { 
            "type": "string",
            "enum": ["grams", "ml", "pieces", "teaspoons", "tablespoons"]
            },
            "amount": { "type": "number" }
        },
        "required": ["name", "unit", "amount"]
        }
    },
    "instructions": {
        "type": "array",
        "description": "Steps to prepare the recipe (no numbering)",
        "items": { "type": "string" }
    },
    "time_to_cook": {
        "type": "number",
        "description": "Total time to prepare the recipe in minutes"
    }
    },
    "required": ["ingredients", "instructions", "time_to_cook"]
    }


# define the function
def get_recipe(dish_type,ingredients,recipe_type):
    if recipe_type:
        recipe_type = "vegetarian"
    else:
        recipe_type = ''
    conversation=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": f"Provide a {recipe_type} {dish_type} recipe containing {ingredients}."}
                  ]
    response = openai.ChatCompletion.create(model="gpt-4", 
                                            messages=conversation, 
                                            functions=[{"name": "set_recipe", "parameters": schema}],
                                            function_call={"name": "set_recipe"},
                                            temperature=0.3
                                            )
    answer = json.loads(response.choices[0].message.function_call.arguments)
    
    return answer


#create an image using DALL-E
def get_image(title):
    PROMPT = f"{title} gourmet cook book photo"

    response = openai.Image.create(
        prompt=PROMPT,
        n=1,
        size="256x256",
    )
    
    if "data" in response:
        for key, obj in enumerate(response["data"]):
            id = obj['url'].split("img-")[1].split(".png")[0]
            filename = os.path.join(app.root_path, 'static', 'img', f'{id}_recipe_image.png')
            print(filename)
            urllib.request.urlretrieve(obj['url'], filename)
        print('Images have been downloaded and saved locally')
    else:
        print("Failed to generate image")
    return f'{str(id)}_recipe_image.png'


"""
{'title': 'Honey Glazed Pork and Carrots', 'ingredients': [{'name': 'pork loin', 'unit': 'grams', 'amount': 500}, {'name': 'carrots', 'unit': 'pieces', 'amount': 4}, {'name': 'honey', 'unit': 'tablespoons', 'amount': 3}, {'name': 'olive oil', 'unit': 'tablespoons', 'amount': 2}, {'name': 'salt', 'unit': 'teaspoons', 'amount': 1}, {'name': 'pepper', 'unit': 'teaspoons', 'amount': 1}], 'instructions': ['Preheat your oven to 375 degrees F (190 degrees C).', 'Peel the carrots and cut them into 2-inch pieces.', 'In a large oven-safe pan, heat the olive oil over medium-high heat. Add the pork loin to the pan and sear on all sides until browned.', 'Remove the pork from the pan and set it aside. Add the carrots to the pan and cook for 5 minutes, stirring occasionally.', 'Return the pork to the pan and drizzle the honey over the pork and carrots. Season with salt and pepper.', 'Place the pan in the preheated oven and roast for 25-30 minutes, or until the pork is cooked through and the carrots are tender.', 'Remove from the oven and let the pork rest for a few minutes before slicing. Serve the pork and carrots with the pan juices drizzled over the top.'], 'time_to_cook': 60}"""