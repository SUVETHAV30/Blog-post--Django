from django.contrib import admin
from .models import Blog, Comment, Reaction, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'blog', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author', 'content')
    date_hierarchy = 'created_at'

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('blog', 'reaction_type', 'user_ip', 'created_at')
    list_filter = ('reaction_type', 'created_at')
    search_fields = ('blog__title', 'user_ip')
    date_hierarchy = 'created_at'
