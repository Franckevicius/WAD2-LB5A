import os
from typing import List, Dict


os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'recipe_sharing.settings')

import django
django.setup()

from main_app.models import Ingredient, UserProfile, Recipe, Comment, RecipeToIngredient, Tag
from django.contrib.auth.models import User


def create_ingredient(name:str, units:str):    
    print(name, units)
    u = Ingredient.objects.get_or_create(name=name, units=units)[0]
    u.save()
    return u


def create_user(username:str, email:str, password:str, about_me:str):    
    django_default_user, is_new_user = User.objects.get_or_create(username=username, email=email)
    if is_new_user:
        django_default_user.set_password(password)
    u = UserProfile.objects.get_or_create(user=django_default_user, about_me=about_me)[0]
    u.save()
    return u


def create_recipe(author:UserProfile, title:str, description:str,  estimated_nutrition:int,
                  estimated_price:int, minutes_to_prepare:int, picture:str,
                  users_who_saved: List[UserProfile], tags: List[Tag]):
    r = Recipe.objects.get_or_create(author=author, title=title, description=description, estimated_nutrition=estimated_nutrition, 
                                     estimated_price=estimated_price, minutes_to_prepare=minutes_to_prepare)[0]    
    r.picture = picture
    r.users_who_saved.set(users_who_saved)
    r.tags.set(tags)
    r.save()
    return r


def map_ingredient_quantities_to_recipe(recipe:Recipe, ingredients:List[Ingredient], ingredients_quantities:List[int]):
    maps = []
    for ingredient, ingredient_quantity in zip(ingredients, ingredients_quantities):
        recipe_ingredient_map = RecipeToIngredient(recipe=recipe, ingredient=ingredient, ingredient_quantity=ingredient_quantity)
        recipe_ingredient_map.save()    
        maps.append(recipe_ingredient_map)
    return maps


def create_comment(content:str, author:UserProfile, recipe:Recipe, parent_comment:Comment):
    c = Comment.objects.get_or_create(content=content, author=author, recipe=recipe)[0]
    c.parent_comment = parent_comment
    c.save()
    return c


def populate():
    #replace duplicate lists and instead query Django object sets -- do they retain order?
    ingredient_objects, user_objects, recipe_objects, ingredient_quantity_maps, comments = [], [], [], [], []
    
    ingredient_data = [
        {"name":"Sausage", "units":"whole" },
        {"name":"Bacon", "units":"strip" },
        {"name":"Mushroom", "units":"whole" },
        {"name":"Tomato", "units":"g" },
        {"name":"Black pudding", "units":"g" },
        {"name":"Egg", "units":"whole" },
        {"name":"Bread", "units":"slice" },
        {"name":"Flour", "units":"g" },
        {"name":"Cornstarch", "units":"g" },
        {"name":"Baking powder", "units":"teaspoon" },
        {"name":"Salt", "units":"pinch" },
        {"name":"Pepper", "units":"pinch" },
        {"name":"Dark beer", "units":"ml" },
        {"name":"Sparkling water", "units":"ml" },
        {"name":"Fish fillet", "units":"g" },
        {"name":"Potato", "units":"g" },
        {"name":"Oil", "units":"ml" },
        {"name":"Spaghetti", "units":"g" },        
        {"name":"Garlic", "units":"clove" },
        {"name":"Sugar", "units":"g" },
        {"name":"Parsley", "units":"g" },
        {"name":"Garlic powder", "units":"g" },
        {"name":"Oregano", "units":"g" },
        {"name":"Basil", "units":"g" },
        {"name":"Capers", "units":"g" },
        {"name":"Beef", "units":"g" },
        {"name":"Onion", "units":"g" },
        {"name":"Tomato paste", "units":"g" },
        {"name":"Tomato sauce", "units":"g" },
        {"name":"Water", "units":"ml" },
        {"name":"Fennel seeds", "units":"g" },
        {"name":"Italian seasoning", "units":"g" },
        {"name":"Lasagna noodles", "units":"sheet" },
        {"name":"Ricotta", "units":"g" },        
        {"name":"Mozarella", "units":"g" },
        {"name":"Parmesan", "units":"g" },
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

    tags = []
    for t in ["British", "Meat", "Breakfast", "Spicy", "Italian"]:
        tag = Tag(content=t)
        tag.save()
        tags.append(tag)

    recipe_data = [
        {
            "author":user_objects[0],
            "title":"British breakfast",
            "ingredients": [ ingredient_objects[0], ingredient_objects[1], ingredient_objects[2], ingredient_objects[3], ingredient_objects[4], ingredient_objects[5] ],
            "ingredients_quantities":[ 2, 3, 2, 300, 60, 2, 1 ], 
            "description":"""Heat the flat grill plate over a low heat, on top of 2 rings/flames if it fits, and brush sparingly with light olive oil.Cook the sausages first.\n\n
                             Add the sausages to the hot grill plate/the coolest part if there is one and allow to cook slowly for about 15-20 minutes, turning occasionally, until golden. After the first 10 minutes, increase the heat to medium before beginning to cook the other ingredients. If you are struggling for space, completely cook the sausages and keep hot on a plate in the oven. \n\n
                             Snip a few small cuts into the fatty edge of the bacon. Place the bacon straight on to the grill plate and fry for 2-4 minutes each side or until your preferred crispiness is reached. Like the sausages, the cooked bacon can be kept hot on a plate in the oven. \n\n
                             For the mushrooms, brush away any dirt using a pastry brush and trim the stalk level with the mushroom top. Season with salt and pepper and drizzle over a little olive oil. Place stalk-side up on the grill plate and cook for 1-2 minutes before turning and cooking for a further 3-4 minutes. Avoid moving the mushrooms too much while cooking, as this releases the natural juices, making them soggy.\n\n
                             For the tomatoes, cut the tomatoes across the centre/or in half lengthways if using plum tomatoes , and with a small, sharp knife remove the green 'eye'. Season with salt and pepper and drizzle with a little olive oil. Place cut-side down on the grill plate and cook without moving for 2 minutes. Gently turn over and season again. Cook for a further 2-3 minutes until tender but still holding their shape.\n\n
                             For the black pudding, cut the black pudding into 3-4 slices and remove the skin. Place on the grill plate and cook for 1½-2 minutes each side until slightly crispy. \n\n
                             For 'proper' fried bread it's best to cook it in a separate pan. Ideally, use bread that is a couple of days old. Heat a frying pan to a medium heat and cover the base with oil. Add the bread and cook for 2-3 minutes each side until crispy and golden. If the pan becomes too dry, add a little more oil. For a richer flavour, add a knob of butter after you turn the slice.\n\n
                             For the fried eggs, break the egg straight into the pan with the fried bread and leave for 30 seconds. Add a good knob of butter and lightly splash/baste the egg with the butter when melted. Cook to your preferred stage, season and gently remove with a fish slice.\n\n
                             Once all the ingredients are cooked, serve on warm plates and enjoy straight away with a good squeeze of tomato ketchup or brown sauce.""", 
            "estimated_nutrition":3, 
            "estimated_price":2, 
            "minutes_to_prepare":60,
            "picture":"recipe1.jpg",
            "users_who_saved":[user_objects[1], user_objects[2]],
            "tags":[tags[0], tags[1], tags[2]]
        },
        {
            "author":user_objects[1],
            "title":"Fish and Chips",
            "ingredients": [ ingredient_objects[7], ingredient_objects[8], 
                             ingredient_objects[9], ingredient_objects[10], ingredient_objects[11], ingredient_objects[12],
                             ingredient_objects[13], ingredient_objects[14], ingredient_objects[15], ingredient_objects[16] ],
            "ingredients_quantities":[ 55, 55, 6, 2, 1, 80, 80, 800, 900, 1000 ], 
            "description":"""Set aside 2 tablespoons of flour. In a large, roomy bowl, mix the remaining flour with the cornstarch and baking powder. Season lightly with a tiny pinch of salt and pepper.\n\n
                             Using a fork to whisk continuously, add the beer and the sparkling water to the flour mixture and continue mixing until you have a thick, smooth batter. Place the batter in the fridge to rest for between 30 minutes and 1 hour.\n\n
                             Meanwhile, cut the potatoes into a little less than 1/2-inch-thick slices, then slice these into 1/2-inch-wide chips. Place the chips into a colander and rinse under cold running water.\n\n
                             Place the washed chips into a pan of cold water. Bring to a gentle boil and simmer for 3 to 4 minutes.\n\n
                             Drain carefully through a colander, then dry with paper towels. Keep in the fridge covered with paper towels until needed.\n\n
                             Meanwhile, lay the fish fillets on a paper towel and pat dry. Season lightly with a little sea salt.\n\n
                             Heat the oil to 350 F in a deep-fat fryer or large, deep saucepan. Cook the chips a few handfuls at a time in the fat for about 2 minutes. Do not brown them. Once the chips are slightly cooked, remove them from the fat and drain. Keep to one side.\n\n
                             Place the 2 tablespoons of flour reserved from the batter mix into a shallow bowl. Toss each fish fillet in the flour and shake off any excess.\n\n
                             Dip into the batter, coating the entire fillet.\n\n
                             Check that the oil temperature is still 350 F. Carefully lower each fillet into the hot oil. Fry for approximately 8 minutes, or until the batter is crisp and golden, turning the fillets from time to time with a large slotted spoon.\n\n
                             Once cooked, remove the fillets from the hot oil and drain on paper towels. Sprinkle with salt. Cover with greaseproof paper (parchment paper) and keep hot.\n\n
                             Serve immediately with the hot fish accompanied by your favorite condiment.""", 
            "estimated_nutrition":1, 
            "estimated_price":2, 
            "minutes_to_prepare":85,
            "picture":"recipe2.jpg",
            "users_who_saved":[user_objects[0]],
            "tags":[tags[0], tags[1]]
        },
        {
            "author":user_objects[2], 
            "title":"Spaghetti Marinara", 
            "ingredients": [ingredient_objects[17], ingredient_objects[3],  ingredient_objects[18], ingredient_objects[19],
                            ingredient_objects[20], ingredient_objects[21], ingredient_objects[10], ingredient_objects[22],
                            ingredient_objects[23], ingredient_objects[11]],
            "ingredients_quantities":[ 450, 900, 1, 11, 11, 5, 1, 1, 20, 2],
            "description":"""In a large saucepan combine crushed tomatoes, diced tomatoes, tomato sauce, minced garlic, sugar, parsley, garlic powder, salt, oregano, basil, and ground black pepper. Add capers and crushed red pepper if desired. Cover. Bring to a boil.\n\n
                             Lower heat and simmer, with cover, for 45 to 60 minutes.\n\n
                             As simmering time nears, in a large pot with boiling salted water cook spaghetti until al dente.\n\n
                             Toss spaghetti with cooked sauce. Serve warm.""", 
            "estimated_nutrition":3,
            "estimated_price":1,
            "minutes_to_prepare":90,
            "picture":"recipe3.jpg",
            "users_who_saved":[],
            "tags":[tags[4]]
        },
        {
            "author":user_objects[3],
            "title":"Lasagna", 
            "ingredients": [ingredient_objects[0], ingredient_objects[25], ingredient_objects[26], ingredient_objects[18],
                            ingredient_objects[3], ingredient_objects[27], ingredient_objects[28], ingredient_objects[29],
                            ingredient_objects[19], ingredient_objects[23], ingredient_objects[30], ingredient_objects[31], 
                            ingredient_objects[10], ingredient_objects[11], ingredient_objects[20], ingredient_objects[32],
                            ingredient_objects[33], ingredient_objects[5], ingredient_objects[34], ingredient_objects[35]],
            "ingredients_quantities":[ 450, 340, 130, 2, 800, 170, 185, 120, 15, 9, 3, 6, 3, 2, 70, 16, 450, 1, 340, 300 ], 
            "description":"""In a Dutch oven, cook sausage, ground beef, onion, and garlic over medium heat until well browned. Stir in crushed tomatoes, tomato paste, tomato sauce, and water. Season with sugar, basil, fennel seeds, Italian seasoning, 1 teaspoon salt, pepper, and 2 tablespoons parsley. Simmer, covered, for about 1 1/2 hours, stirring occasionally.\n\n
                             Bring a large pot of lightly salted water to a boil. Cook lasagna noodles in boiling water for 8 to 10 minutes. Drain noodles, and rinse with cold water. In a mixing bowl, combine ricotta cheese with egg, remaining parsley, and 1/2 teaspoon salt.\n\n
                             Preheat oven to 375 degrees F (190 degrees C).\n\n
                             To assemble, spread 1 1/2 cups of meat sauce in the bottom of a 9x13-inch baking dish. Arrange 6 noodles lengthwise over meat sauce. Spread with one half of the ricotta cheese mixture. Top with a third of mozzarella cheese slices. Spoon 1 1/2 cups meat sauce over mozzarella, and sprinkle with 1/4 cup Parmesan cheese. Repeat layers, and top with remaining mozzarella and Parmesan cheese. Cover with foil: to prevent sticking, either spray foil with cooking spray, or make sure the foil does not touch the cheese.\n\n
                             Bake in preheated oven for 25 minutes. Remove foil, and bake an additional 25 minutes. Cool for 15 minutes before serving.""", 
            "estimated_nutrition":2, 
            "estimated_price":2,
            "minutes_to_prepare":195,
            "picture":"recipe4.jpg",
            "users_who_saved":[user_objects[0], user_objects[1], user_objects[2]],
            "tags":[]
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
        {"content":"Comment1", "author":user_objects[0], "recipe":recipe_objects[0], "parent_comment":None},
        {"content":"Comment2", "author":user_objects[1], "recipe":recipe_objects[0], "parent_comment":None},
        {"content":"Comment3", "author":user_objects[2], "recipe":recipe_objects[2], "parent_comment":None},
        {"content":"Comment4", "author":user_objects[3], "recipe":recipe_objects[3], "parent_comment":None},
    ]

    for comment in comment_data:
        comments.append(create_comment(**comment))

    #could add constraints that replies must be made on the same recipe page, but will most likely
    #be automatically enforced client-side
    replies_data = [
        {"content":"Comment5", "author":user_objects[1], "recipe":recipe_objects[0], "parent_comment":comments[0]},
        {"content":"Comment6", "author":user_objects[2], "recipe":recipe_objects[0], "parent_comment":comments[0]},
        {"content":"Comment7", "author":user_objects[3], "recipe":recipe_objects[0], "parent_comment":comments[1]},
    ]

    for reply in replies_data:
        comments.append(create_comment(**reply))

    for comment in Comment.objects.all():
        print(comment)

if __name__ == "__main__":
    populate()
