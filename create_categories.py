import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from blog.models import Category

# Create initial categories
categories = [
    {
        'name': 'Technology',
        'slug': 'technology',
        'description': 'Posts about technology and innovation'
    },
    {
        'name': 'Food',
        'slug': 'food',
        'description': 'Posts about food and recipes'
    },
    {
        'name': 'Travel',
        'slug': 'travel',
        'description': 'Posts about travel experiences'
    },
    {
        'name': 'Lifestyle',
        'slug': 'lifestyle',
        'description': 'Posts about lifestyle and daily living'
    }
]

for category_data in categories:
    Category.objects.get_or_create(
        name=category_data['name'],
        defaults={
            'slug': category_data['slug'],
            'description': category_data['description']
        }
    )

print("Categories created successfully!") 