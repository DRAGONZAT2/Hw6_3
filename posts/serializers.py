from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')  # чтобы видеть email владельца

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'owner', 'created_at')
        read_only_fields = ['owner', 'created_at']
