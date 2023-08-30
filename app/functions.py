
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
    "prompt": {
        "type": "string",
        "description": "a prompt for DALL-E to generate a high qualtiy picture of the recipe in the style of modern food photography, 15mm, warm light"
    },
    "ingredients": {
        "type": "array",
        "items": {
        "type": "object",
        "properties": {
            "name": { "type": "string" },
            "unit": { 
            "type": "string",
            "enum": ["grams", "ml","l","pinch","pieces", "teaspoons", "tablespoons"]
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
    "required": ["title","ingredients", "instructions", "time_to_cook", "prompt"]
    }


# define the function
def get_recipe(dish_type,ingredients,recipe_type):
    if recipe_type:
        recipe_type = "vegetarian"
    else:
        recipe_type = ''
    conversation=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": f"Provide a healthy {recipe_type} {dish_type} recipe containing {ingredients}. Add other ingredients if you think this would make the dish better."}
                  ]
    response = openai.ChatCompletion.create(model="gpt-4", 
                                            messages=conversation, 
                                            functions=[{"name": "set_recipe", "parameters": schema}],
                                            function_call={"name": "set_recipe"},
                                            temperature=0.5
                                            )
    answer = json.loads(response.choices[0].message.function_call.arguments)
    
    return answer


#create an image using DALL-E
def get_image(title):
    PROMPT = f"{title} food photography, 15mm, warm light"

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