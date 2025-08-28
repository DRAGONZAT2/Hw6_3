from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tags', views.TagViewSet, basename='tag')
router.register(r'ingredients', views.IngredientViewSet, basename='ingredient')
router.register(r'recipes', views.RecipeViewSet, basename='recipe')

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:recipe_pk>/comments/', views.RecipeCommentsViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='recipe-comments'),


    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),

    path('shopping-list/', views.ShoppingListCreateView.as_view(), name='shopping-list'),
]