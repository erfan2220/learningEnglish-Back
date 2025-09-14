from rest_framework import serializers
from .models import BlogPost, BlogBlock


class BlogBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogBlock
        fields = ["id", "block_type", "content", "image", "video_url", "order"]


class BlogPostSerializer(serializers.ModelSerializer):
    blocks = BlogBlockSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = ["id", "title", "slug", "author", "created_at", "updated_at", "blocks"]
