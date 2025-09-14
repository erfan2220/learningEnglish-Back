from django.db import models
from django.conf import settings

...
author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BlogBlock(models.Model):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"

    BLOCK_TYPES = [
        (TEXT, "متن"),
        (IMAGE, "تصویر"),
        (VIDEO, "ویدیو"),
    ]

    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="blocks")
    block_type = models.CharField(max_length=10, choices=BLOCK_TYPES, default=TEXT)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="blog/images/", blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.post.title} - {self.block_type}"
