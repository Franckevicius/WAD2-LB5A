import os
from tokenize import String
from typing import List, Dict

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'recipe_sharing.settings')

import django
django.setup()

from main_app.models import Ingredient, UserProfile, Recipe, Comment, RecipeToIngredient
from django.contrib.auth.models import User


def create_ingredient(name:str, units:str):    
    print(name, units)
    u = Ingredient.objects.get_or_create(name=name, units=units)[0]
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


def create_recipe(author:UserProfile, title:str, description:str,  estimated_nutrition:int,
                  estimated_price:int, minutes_to_prepare:int, picture:str):
    r = Recipe.objects.get_or_create(author=author, title=title, description=description, estimated_nutrition=estimated_nutrition, 
                                     estimated_price=estimated_price, minutes_to_prepare=minutes_to_prepare)[0]    
    r.picture = picture
    r.save()
    return r


def map_ingredient_quantities_to_recipe(recipe:Recipe, ingredients:List[Ingredient], ingredients_quantities:List[int]):
    maps = []
    for ingredient, ingredient_quantity in zip(ingredients, ingredients_quantities):
        recipe_ingredient_map = RecipeToIngredient(recipe=recipe, ingredient=ingredient, ingredient_quantity=ingredient_quantity)
        recipe_ingredient_map.save()    
        maps.append(recipe_ingredient_map)
    return maps


def create_comment(content:str, author:UserProfile, recipe:Recipe):
    c = Comment.objects.get_or_create(content=content, author=author, recipe=recipe)[0]
    c.save()
    return c


def populate():
    #replace duplicate lists and instead query Django object sets -- do they retain order?
    ingredient_objects, user_objects, recipe_objects, ingredient_quantity_maps = [], [], [], []
    
    ingredient_data = [
        {"name":"Water", "units":"ml" },
        {"name":"Tomato", "units":"g" },
        {"name":"Potato", "units":"g" },
        {"name":"Salt", "units":"g" },        
    ]

    user_data = [
        {"username":"User1", "email":"User1@email.com", "password":"user1password", "about_me":"User1_about_me"},
        {"username":"User2", "email":"User2@email.com", "password":"user2password", "about_me":"User2_about_me"},
        {"username":"User3", "email":"User3@email.com", "password":"user3password", "about_me":"User3_about_me"},
        {"username":"User4", "email":"User4@email.com", "password":"user4password", "about_me":"User4_about_me"}
    ]

    for ingredient in ingredient_data:
        ingredient_objects.append(create_ingredient(**ingredient))

    for ingredient in Ingredient.objects.all():
        print(ingredient)


    for user in user_data:
        user_objects.append(create_user(**user))

    for user in UserProfile.objects.all():
        print(user)

    recipe_data = [
        {
            "author":user_objects[0],
            "title":"Recipe1",
            "ingredients": [ ingredient_objects[0], ingredient_objects[1] ],
            "ingredients_quantities":[ 100, 200 ], 
            "description":"desc1", 
            "estimated_nutrition":1, 
            "estimated_price":1, 
            "minutes_to_prepare":15,
            "picture":"pictures_placeholder/1.png"
        },
        {
            "author":user_objects[1],
            "title":"Recipe2",
            "ingredients": [ ingredient_objects[1], ingredient_objects[2] ],
            "ingredients_quantities":[ 250, 350 ], 
            "description":"desc2", 
            "estimated_nutrition":2, 
            "estimated_price":2, 
            "minutes_to_prepare":25,
            "picture":"pictures_placeholder/2.png"
        },
        {
            "author":user_objects[2], 
            "title":"Recipe3", 
            "ingredients": [ingredient_objects[2], ingredient_objects[3] ],
            "ingredients_quantities":[ 100, 100 ],
            "description":"desc3", 
            "estimated_nutrition":3,
            "estimated_price":3,
            "minutes_to_prepare":35,
            "picture":"pictures_placeholder/3.png"
        },
        {
            "author":user_objects[3],
            "title":"Recipe4", 
            "ingredients": [ingredient_objects[3], ingredient_objects[1] ],
            "ingredients_quantities":[ 100, 50 ], 
            "description":"desc4", 
            "estimated_nutrition":2, 
            "estimated_price":2,
            "minutes_to_prepare":45,
            "picture":"pictures_placeholder/4.png"
        },        
    ]

    for recipe in recipe_data:
        r = create_recipe(**({k:v for k,v in recipe.items() if not k.startswith("ingredient") }))
        recipe_objects.append(r)
        ingredient_quantity_maps.append(
            map_ingredient_quantities_to_recipe(r, recipe["ingredients"], recipe["ingredients_quantities"])
        )

    for i, recipe in enumerate(Recipe.objects.all()):
        print(recipe)
        for ingredient_quantity in ingredient_quantity_maps[i]:
            print(ingredient_quantity)


    comment_data = [
        {"content":"Comment1", "author":user_objects[0], "recipe":recipe_objects[0]},
        {"content":"Comment1", "author":user_objects[1], "recipe":recipe_objects[1]},
        {"content":"Comment1", "author":user_objects[2], "recipe":recipe_objects[2]},
        {"content":"Comment1", "author":user_objects[3], "recipe":recipe_objects[3]},
    ]

    for comment in comment_data:
        create_comment(**comment)

    for comment in Comment.objects.all():
        print(comment)

if __name__ == "__main__":
    populate()
