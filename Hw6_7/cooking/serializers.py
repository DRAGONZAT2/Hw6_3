from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction
from rest_framework import serializers
from django.db.models import Avg, Count

from .models import (
    Tag, Ingredient, Recipe, RecipeIngredient,
    Favorite, Comment, Rating
)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'unit')

class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'amount')

class RecipeIngredientWriteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=8, decimal_places=1, min_value=Decimal('0.1'))

class RecipeReadSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    avg_rating = serializers.FloatField(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    comments_count = serializers.IntegerField(read_only=True)
    steps = serializers.JSONField()

    class Meta:
        model = Recipe
        fields = ('id','author','title','description','image','tags','ingredients',
                  'steps','time_minutes','created_at','avg_rating','is_favorited','comments_count')

    def get_ingredients(self, obj):
        qs = obj.recipe_ingredients.select_related('ingredient').all()
        return RecipeIngredientReadSerializer(qs, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

class RecipeWriteSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(), write_only=True)
    ingredients = RecipeIngredientWriteSerializer(many=True, write_only=True)
    steps = serializers.ListField(child=serializers.CharField(), allow_empty=False)

    class Meta:
        model = Recipe
        fields = ('title','description','image','tags','ingredients','steps','time_minutes')

    def validate_time_minutes(self, value):
        if not (1 <= value <= 600):
            raise serializers.ValidationError("time_minutes must be 1..600")
        return value

    def validate_ingredients(self, value):
        ids = [item['id'] for item in value]
        if len(ids) != len(set(ids)):
            raise serializers.ValidationError("Duplicate ingredients are not allowed")
        for item in value:
            amount = Decimal(item['amount'])
            if amount < Decimal('0.1'):
                raise serializers.ValidationError("Ingredient amount must be >= 0.1")
        return value

    def validate_tags(self, value):
        if not value or len(value) < 1:
            raise serializers.ValidationError("At least one tag is required")
        return value

    @transaction.atomic
    def create(self, validated_data):
        tags_names = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        steps = validated_data.pop('steps', [])
        author = self.context['request'].user

        recipe = Recipe.objects.create(author=author, steps=steps, **validated_data)
       
        from django.utils.text import slugify
        tag_objs = []
        for name in tags_names:
            slug = slugify(name)
            tag_obj, _ = Tag.objects.get_or_create(slug=slug, defaults={'name': name})
            tag_objs.append(tag_obj)
        recipe.tags.set(tag_objs)

        for item in ingredients_data:
            ing = Ingredient.objects.get(pk=item['id'])
            amt = (Decimal(item['amount']).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ing, amount=amt)
        return recipe
    
    @transaction.atomic
    def update(self, instance, validated_data):
        tags_names = validated_data.pop('tags', None)
        ingredients_data = validated_data.pop('ingredients', None)
        steps = validated_data.pop('steps', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if steps is not None:
            instance.steps = steps
        instance.save()

        from django.utils.text import slugify
        if tags_names is not None:
            tag_objs = []
            for name in tags_names:
                slug = slugify(name)
                tag_obj, _ = Tag.objects.get_or_create(slug=slug, defaults={'name': name})
                tag_objs.append(tag_obj)
            instance.tags.set(tag_objs)

        if ingredients_data is not None:
            instance.recipe_ingredients.all().delete()
            for item in ingredients_data:
                ing = Ingredient.objects.get(pk=item['id'])
                amt = (Decimal(item['amount']).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))
                RecipeIngredient.objects.create(recipe=instance, ingredient=ing, amount=amt)
        return instance

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user','recipe')

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id','recipe','author','text','created_at','updated_at')
        read_only_fields = ('recipe','author','created_at','updated_at')

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment text cannot be empty")
        if len(value) > 2000:
            raise serializers.ValidationError("Max 2000 characters")
        return value

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id','recipe','user','value')
        read_only_fields = ('recipe','user')
    def validate_value(self, v):
        if not (1 <= v <= 5):
            raise serializers.ValidationError("Rating must be 1..5")
        return v
