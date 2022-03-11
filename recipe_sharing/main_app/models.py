from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique=True)
    quantity = models.PositiveSmallIntegerField(default=0)
    units = models.CharField(max_length=32) #e.g. grams, milliliters
 

    def __str__(self):
        return f"{self.name}: {self.quantity}{self.units}"


    class Meta:
        verbose_name_plural = 'Ingredients'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # stores username, password, email
    about_me = models.CharField(max_length=256)


    def __str__(self):
        return self.user.username


    class Meta:
        verbose_name_plural = 'UserProfiles'


class Recipe(models.Model):    
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)    
    title = models.CharField(max_length=128)
    title_slug = models.SlugField()
    ingredients = models.ManyToManyField(Ingredient)
    description = models.CharField(max_length=4096)    
    estimated_nutrition = models.SmallIntegerField(default=1) #Ranges [1-3]
    estimated_price = models.SmallIntegerField(default=1) #Ranges [1-3]
    minutes_to_prepare = models.SmallIntegerField(default=0) 
    picture = models.ImageField(upload_to='recipe_images', blank=True) #Located at "/media/<upload_to>"
        

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)


    def __str__(self):
        return self.title


    class Meta:
        verbose_name_plural = 'Recipes'


class Comment(models.Model):
    content = models.CharField(max_length=4096)
    time_posted = models.DateTimeField(auto_now_add=True) # Save creation timestamp
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)    
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE) # Consider on_delete SET_DEFAULT
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.time_posted} by {str(self.author)}"


    class Meta:
        verbose_name_plural = 'UserProfiles'