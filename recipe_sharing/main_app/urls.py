from django.urls import path
from main_app import views

app_name = 'main_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('recipe/<slug:recipe_title_slug>/',
         views.render_recipe, name='render_recipe'),
    #path('register', views.register, name='register'),
    #path('login/', views.user_login, name='login'),
    #path('my-profile/', views.user_profile, name='my-profile'),
    #path('my-profile/saved/', views.profile_saved, name='profile_saved'),
    #path('search/', views.search, name='search'),
    #path('submit/', views.submit, name='submit'),
]