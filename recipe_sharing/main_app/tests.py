from django.test import TestCase
from .models import UserProfile, Ingredient, Tag, Recipe
from django.db.utils import IntegrityError
from django.contrib.auth.models import User


class IngredientTests(TestCase):
    def test_ensure_ingredient_names_unique(self): 
        """
        Ensures ingredients with duplicate names cannot be created.
        """
        i = Ingredient(name="apple", units="g")
        i.save()
        try:
            i = Ingredient(name="apple", units="kg")
            i.save()
        except IntegrityError as e:
            pass
        finally:
            self.failUnlessRaises(IntegrityError)        


class TagTests(TestCase):
    def test_ensure_tag_name_lowercase(self): 
        """
        Ensures tags are saved in lowercase
        """
        t = Tag(content="Italian")
        t.save()
        self.assertEquals(t.content, "italian")
    

    def test_tag_contents_unique(self): 
        """
        Ensures duplicate tags cannot be created.
        """
        t= Tag(content="Spicy")
        t.save()
        try:
            t= Tag(content="spicy")
            t.save()
        except IntegrityError as e:
            pass
        finally:
            self.failUnlessRaises(IntegrityError)   


class RecipeTests(TestCase):
    def test_slug_creation(self): 
        """
        Ensures correct slugs are created
        """
        user = User(username="John", email="john@email.com")
        user.save()
        author = UserProfile(user=user, about_me="I'm John")
        author.save()
        r = Recipe(title="Spicy spaghetti meatballs", description="I make this every day!", author=author,
                  estimated_nutrition=1, estimated_price=1, minutes_to_prepare=20)
        r.save()
        self.assertEquals(r.title_slug, "spicy-spaghetti-meatballs")