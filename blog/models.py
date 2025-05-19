from django.db import models
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def post_count(self):
        return self.blogs.count()

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='blogs')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

    @property
    def reaction_counts(self):
        return {
            'heart': self.reactions.filter(reaction_type='heart').count(),
            'insightful': self.reactions.filter(reaction_type='insightful').count(),
            'funny': self.reactions.filter(reaction_type='funny').count(),
        }

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author} on {self.blog.title}'

    @property
    def is_reply(self):
        return self.parent is not None

class Reaction(models.Model):
    REACTION_CHOICES = [
        ('heart', '❤️'),
        ('insightful', '💡'),
        ('funny', '😂'),
    ]
    
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    user_ip = models.GenericIPAddressField()  # To track unique reactions

    class Meta:
        unique_together = ['blog', 'user_ip', 'reaction_type']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_reaction_type_display()} on {self.blog.title}"
