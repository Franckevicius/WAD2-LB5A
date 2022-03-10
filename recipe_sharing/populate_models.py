import os
from tokenize import String
from typing import List

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'recipe_sharing.settings')

import django
django.setup()

from main_app.models import Ingredient, UserProfile, Recipe, Comment
from django.contrib.auth.models import User


def create_ingredient(name:str, quantity:int, units:str):
    u = Ingredient.objects.get_or_create(name=name, quantity=quantity, units=units)[0]
    u.save()
    return u


def create_user(username:str, email:str, password:str, about_me:str):
    # Will break if user already exists/duplicate info
    # Short workaround - delete db, make migration, migrate
    # Longterm - add handling to detect if such user already exists, or don't use manager and add custom initialization
    django_user = User.objects.create_user(username, email, password) 
    u = UserProfile.objects.get_or_create(user=django_user, about_me=about_me)[0]
    u.save()
    return u


def create_recipe(title:str, ingredients:List[Ingredient], description:str, 
                  estimated_nutrition:int, estimated_price:int, minutes_to_prepare:int, picture:str):
    r = Recipe.objects.get_or_create(title=title, description=description, estimated_nutrition=estimated_nutrition, 
                                      estimated_price=estimated_price, minutes_to_prepare=minutes_to_prepare)[0]
    r.picture = picture
    r.ingredients = ingredients
    r.save()
    return r


def populate():
    ingredient_objects, user_objects, recipe_objects = [], [], []
    
    ingredients = [
        {"name":"Water", "quantity":100, "units":"ml" },
        {"name":"Tomato", "quantity":200, "units":"g" },
        {"name":"Potato", "quantity":500, "units":"g" },
        {"name":"Salt", "quantity":5, "units":"g" },
    ]

    users = [
        {"username":"User1", "email":"User1@email.com", "password":"user1password", "about_me":"User1_about_me"},
        {"username":"User2", "email":"User2@email.com", "password":"user2password", "about_me":"User2_about_me"},
        {"username":"User3", "email":"User3@email.com", "password":"user3password", "about_me":"User3_about_me"},
        {"username":"User4", "email":"User4@email.com", "password":"user4password", "about_me":"User4_about_me"}
    ]

    for ingredient in ingredients:
        ingredient_objects.append(create_ingredient(**ingredient))

    for ingredient in Ingredient.objects.all():
        print(ingredient)


    for user in users:
        user_objects.append(create_user(**user))

    for user in UserProfile.objects.all():
        print(user)

    recipes = [
        {"title":"Recipe1", "ingredients":[ingredients[0], ingredients[1]], "description":"desc1", "estimated_nutrition":1, 
         "estimated_price":1, "minutes_to_prepare":15, "picture":"pictures_placeholder/1.png"},
        {"title":"Recipe1", "ingredients":[ingredients[1], ingredients[2]], "description":"desc2", "estimated_nutrition":2, 
         "estimated_price":2, "minutes_to_prepare":25, "picture":"pictures_placeholder/2.png"},
        {"title":"Recipe1", "ingredients":[ingredients[2], ingredients[3]], "description":"desc3", "estimated_nutrition":3, 
         "estimated_price":3, "minutes_to_prepare":35, "picture":"pictures_placeholder/3.png"},
        {"title":"Recipe1", "ingredients":[ingredients[3], ingredients[2]], "description":"desc4", "estimated_nutrition":2, 
         "estimated_price":2, "minutes_to_prepare":45, "picture":"pictures_placeholder/4.png"},
         
    ]

    for recipe in recipes:
        recipes.append(create_recipe(**recipe))

    for recipe in Recipe.objects.all():
        print(recipe)


if __name__ == "__main__":
    populate()
