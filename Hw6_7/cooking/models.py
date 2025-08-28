from django.conf import settings
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

User = settings.AUTH_USER_MODEL


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)


    class Meta:
        ordering = ['name']


    def __str__(self):
     return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=20)

    class Meta:
        unique_together = ('name', 'unit')
        ordering = ['name']


    def __str__(self):
        return f"{self.name} ({self.unit})"


class Recipe(TimestampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='recipes', blank=False)
    steps = models.JSONField(default=list, blank=True)
    time_minutes = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(600)])
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['created_at']


    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredient_in_recipes')
    amount = models.DecimalField(max_digits=8, decimal_places=1, validators=[MinValueValidator(Decimal('0.1'))])

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f"{self.ingredient.name} - {self.amount}{self.ingredient.unit} in {self.recipe.title}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorited_by')
    
    class Meta:
        unique_together = ('user', 'recipe')
    
    def __str__(self):
        return f"{self.user} -> {self.recipe}"
    

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author} on {self.recipe}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    value = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])


    class Meta:
        unique_together = ('user', 'recipe')