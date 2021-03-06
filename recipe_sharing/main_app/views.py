from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
#from main_app.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Recipe, Comment


def index(request):
    context_dict = {}
    context_dict["recipes"] = Recipe.objects.all()    
    return render(request, 'main_app/index.html', context=context_dict)


def render_recipe(request, recipe_title_slug):
    context = {"recipe" : None, "comments" : None}
    try:
        context["recipe"] = Recipe.objects.get(title_slug=recipe_title_slug)
    except Recipe.DoesNotExist:
        pass
    context["comments"] = Comment.objects.filter(recipe=context["recipe"]).order_by("time_posted") #Should get all comments which have this recipe as FK
    return render(request, "main_app/recipe.html", context=context)


def about(request):
    context_dict = {}
    context_dict['boldmessage'] = 'This is the about page'

    response = render(request, 'main_app/about.html', context=context_dict)
    return response


def get_filtered_recipes(search_query):
    recipes = None
    ingredients = [i.strip() for i in str.split(search_query, " ") if i != ""]
    substrings = set()    

    for ingredient in ingredients:        
        if ingredient.isalpha() and ingredient not in substrings:            
            if recipes is None:
                recipes = Recipe.objects.filter(recipetoingredient__ingredient__name__istartswith=ingredient).distinct()
            else:
                recipes &= (Recipe.objects.filter(recipetoingredient__ingredient__name__istartswith=ingredient).distinct())            
            
            for i in range(len(ingredient)):
                substrings.add(ingredient[:i+1])
        
    return recipes


def search(request):    
    search_query = "" if "ingredient_input" not in request.GET else request.GET["ingredient_input"]
    recipes = None if search_query=="" else get_filtered_recipes(search_query)
    #print(request.GET)
    #print(recipes)
    return render(request, "main_app/search.html", {"recipes":recipes})


# def register(request):

#     registered = False

#     if request.method =='POST':
#         user_form = UserForm(request.POST)
#         profile_form = UserProfileForm(request.POST)

#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()

#             user.set_password(user.password)
#             user.save()

#             profile = profile_form.save(commit=False)
#             profile.user = user

#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['pictures']

#             profile.save()

#             registered = True
#         else:
#             print(user_form.errors, profile_form.errors)
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()

#     return render(request,
#                   'main_app/register.html',
#                   context = {'user_form': user_form,
#                              'profile_form': profile_form,
#                              'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('main_app:index'))
            else:
                return HttpResponse("Your Recipe Sharing account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'main_app/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))
