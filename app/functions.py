
import openai
import json
from app import app
import urllib.request
import os
import requests
from bs4 import BeautifulSoup


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
    "recipe_type": {
        "type": "string",
        "description": "wether the recipe is vegetarian, vegan, or with meat",
        "enum": ["vegetarian", "vegan", "meat"]
    }
    },
    "required": ["title","ingredients", "instructions", "recipe_type", "prompt"]
    }


# define the function
def get_recipe(dish_type,ingredients,recipe_type):
    if recipe_type:
        recipe_type = "vegetarian"
    else:
        recipe_type = ''
    conversation=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": f"""Provide a healthy {recipe_type} {dish_type} recipe containing {ingredients}. 
                   Add other ingredients if you think this would make the dish better."""}
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


#function that uses requets lib to extract html of a web page and prettyfies it with bs4
def extract_html(url):
    # Send a GET request to the URL

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    
    # Check if the GET request is successful
    if response.status_code == 200:
        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(response.text, 'html.parser')
        for data in soup(['style', 'script', 'a']):
        # Remove tags
            data.decompose()
        soup = ' '.join(soup.stripped_strings)
        body = soup.find('body')
        # Return the pretty-printed HTML
        return soup
    else:
        return "Failed to retrieve HTML."
    
# define the function
def extract_recipe(html):
    conversation=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": f"extract the recipe form the follwoing html code:\n{html}"}
                  ]
    response = openai.ChatCompletion.create(model="gpt-4", 
                                            messages=conversation, 
                                            functions=[{"name": "set_recipe", "parameters": schema}],
                                            function_call={"name": "set_recipe"},
                                            temperature=0.5
                                            )
    answer = json.loads(response.choices[0].message.function_call.arguments)
    
    return answer