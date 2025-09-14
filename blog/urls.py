from django.urls import path
from .views import BlogPostList, BlogPostDetail

urlpatterns = [
    path('', BlogPostList.as_view(), name='blog-list'),
    path('<slug:slug>/', BlogPostDetail.as_view(), name='blog-detail'),
]
