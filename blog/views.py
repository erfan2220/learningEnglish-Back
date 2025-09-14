from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import BlogPost
from .serializers import BlogPostSerializer


class BlogPostList(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all().order_by("-created_at")
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]  # ← همه می‌تونن ببینن بدون لاگین


class BlogPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = "slug"
    permission_classes = [AllowAny]  # ← همه می‌تونن جزئیات ببینن
