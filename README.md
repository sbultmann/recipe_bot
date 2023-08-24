# Recipe Bot
This is an implementation of a recipe generator based on GPT-4 and DALL-E in flask.

## app/function.py

```Python
import openai
import json
from app import app
import urllib.request
import os

openai.api_key = app.config["OPENAI_API"]

schema = { ... }

def get_recipe(dish_type,ingredients,recipe_type):
    ...
    return answer

def get_image(title):
    ...
    return f'{str(id)}_recipe_image.png'
```

This Python code does the following:

* It sets up a connection to the OpenAI API using a key provided in the app's configuration.
* It defines a `JSON` schema that describes the structure of a recipe, including details like the title, ingredients, instructions, etc.
* It defines a function `get_recipe()` that:
* Takes in 3 arguments: `dish_type`, `ingredients`, and `recipe_type`.
* The recipe_type is checked, if it is present it's set as "vegetarian", otherwise an empty string.
* The function then constructs a conversation structure where the user requests a specific type of dish.
* This conversation is then used as input to `openai.ChatCompletion.create()` function to get a response from OpenAI's gpt-4 model.
* The response is then parsed and returned.
* It defines a function `get_image()` that:
* Takes in a title representing the name of a recipe.
* A prompt is constructed ("food photography, 15mm, warm light") and it's used to generate an image using OpenAI's DALL-E image generator.
* If the image generation is successful, the image is downloaded and saved locally and the file name is returned.
* If the image generation fails, a failure message will be printed.
