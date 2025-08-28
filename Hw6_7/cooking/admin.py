from django.contrib import admin
from django.db.models import Avg, Count
from .models import (
    Tag, Ingredient, Recipe, RecipeIngredient,
    Favorite, Comment, Rating
)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    ordering = ('id',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit')
    search_fields = ('name',)
    ordering = ('id',)
    list_filter = ('unit',)

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'time_minutes', 'avg_rating', 'comments_count', 'created_at')
    search_fields = ('title', 'author__username')
    list_filter = ('tags', 'author')
    inlines = [RecipeIngredientInline]
    ordering = ('-created_at',)

    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(
            _avg_rating=Avg('ratings__value'),
            _comments_count=Count('comments')
        )
        return qs

    def avg_rating(self, obj):
        return round(obj._avg_rating or 0, 1)
    avg_rating.admin_order_field = '_avg_rating'
    avg_rating.short_description = 'Avg Rating'

    def comments_count(self, obj):
        return obj._comments_count
    comments_count.admin_order_field = '_comments_count'
    comments_count.short_description = 'Comments'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user__username', 'recipe__title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'author', 'created_at', 'updated_at')
    search_fields = ('author__username', 'recipe__title', 'text')
    list_filter = ('created_at', 'updated_at')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', 'value')
    search_fields = ('user__username', 'recipe__title')
    list_filter = ('value',)