from django.db.models import Avg, Count, Sum
from django.shortcuts import get_object_or_404
from rest_framework import viewsets,status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .models import Tag, Ingredient, Recipe, Favorite, Comment, Rating, RecipeIngredient
from .serializers import (
    TagSerializer, IngredientSerializer,
    RecipeReadSerializer, RecipeWriteSerializer,
    CommentSerializer, RatingSerializer
)
from .permissions import IsAuthorOrStaff

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    def get_permissions(self):
        if self.request.method in ('POST','PATCH','PUT','DELETE'):
            return [IsAdminUser()]
        return [AllowAny()]

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [SearchFilter]
    search_fields = ['^name']  
    def get_permissions(self):
        if self.request.method in ('POST','PATCH','PUT','DELETE'):
            return [IsAdminUser()]
        return [AllowAny()]

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().select_related('author').prefetch_related('tags')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title']
    ordering_fields = ['time_minutes','created_at']
    pagination_class = StandardPagination

    def get_serializer_class(self):
        if self.action in ('create','update','partial_update'):
            return RecipeWriteSerializer
        return RecipeReadSerializer

    def get_permissions(self):
        if self.action in ('create', 'favorite', 'rating', 'shopping_list'):
            return [IsAuthenticated()]
        if self.action in ('update','partial_update','destroy'):
            return [IsAuthorOrStaff()]
        return [AllowAny()]

    def get_queryset(self):
        qs = super().get_queryset().annotate(
            avg_rating=Avg('ratings__value'),
            comments_count=Count('comments')
        )
        favorited = self.request.query_params.get('favorited')
        if favorited == '1' and self.request.user.is_authenticated:
            qs = qs.filter(favorited_by__user=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post','delete'], permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        recipe = self.get_object()
        if request.method == 'POST':
            Favorite.objects.get_or_create(user=request.user, recipe=recipe)
            return Response(status=status.HTTP_200_OK)
        else:  
            Favorite.objects.filter(user=request.user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post','delete'], permission_classes=[IsAuthenticated])
    def rating(self, request, pk=None):
        recipe = self.get_object()
        if request.method == 'POST':
            value = request.data.get('value')
            if value is None:
                return Response({"detail":"value required"}, status=400)
            try:
                v = int(value)
            except (ValueError, TypeError):
                return Response({"detail":"value must be int 1..5"}, status=400)
            if not (1 <= v <= 5):
                return Response({"detail":"value must be 1..5"}, status=400)
            Rating.objects.update_or_create(user=request.user, recipe=recipe, defaults={'value': v})
            return Response(status=status.HTTP_200_OK)
        else:
            Rating.objects.filter(user=request.user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeCommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrStaff]
    def get_queryset(self):
        recipe_id = self.kwargs.get('recipe_pk') or self.kwargs.get('recipe_id')
        return Comment.objects.filter(recipe_id=recipe_id).select_related('author')

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get('recipe_pk') or self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        serializer.save(author=self.request.user, recipe=recipe)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrStaff]


from rest_framework.views import APIView
class ShoppingListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        fav_recipes = Recipe.objects.filter(favorited_by__user=request.user)
        ing_qs = RecipeIngredient.objects.filter(recipe__in=fav_recipes).values(
            'ingredient'
        ).annotate(total_amount=Sum('amount')).order_by()
        result = []
        for row in ing_qs:
            ingredient = Ingredient.objects.get(pk=row['ingredient'])
            total = row['total_amount'] or 0
            result.append({
                'ingredient': {
                    'id': ingredient.id,
                    'name': ingredient.name,
                    'unit': ingredient.unit
                },
                'amount': float(total)
            })
        return Response(result, status=200)