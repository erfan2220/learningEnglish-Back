from django.contrib import admin
from .models import BlogPost, BlogBlock

class BlogBlockInline(admin.TabularInline):
    model = BlogBlock
    extra = 1

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [BlogBlockInline]

admin.site.register(BlogBlock)
