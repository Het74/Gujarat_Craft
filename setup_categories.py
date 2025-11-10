"""
Script to create initial categories for Gujarat Crafts
Run this script after running migrations: python setup_categories.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gujarat_crafts.settings')
django.setup()

from store.models import Category

# Categories to create
categories_data = [
    {'name': 'Pottery', 'slug': 'pottery', 'description': 'Handcrafted pottery and ceramic items'},
    {'name': 'Textiles', 'slug': 'textiles', 'description': 'Traditional Gujarati textiles and fabrics'},
    {'name': 'Jewelry', 'slug': 'jewelry', 'description': 'Handcrafted jewelry and accessories'},
    {'name': 'Woodwork', 'slug': 'woodwork', 'description': 'Artistic woodwork and furniture'},
    {'name': 'Metalwork', 'slug': 'metalwork', 'description': 'Handcrafted metal items and sculptures'},
    {'name': 'Paintings', 'slug': 'paintings', 'description': 'Traditional and modern paintings'},
    {'name': 'Embroidery', 'slug': 'embroidery', 'description': 'Hand-embroidered items and fabrics'},
    {'name': 'Leather Work', 'slug': 'leather-work', 'description': 'Handcrafted leather goods'},
]

def create_categories():
    """Create categories if they don't exist"""
    created_count = 0
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={
                'name': cat_data['name'],
                'description': cat_data.get('description', '')
            }
        )
        if created:
            created_count += 1
            print(f"Created category: {category.name}")
        else:
            print(f"Category already exists: {category.name}")
    
    print(f"\nTotal categories created: {created_count}")
    print(f"Total categories in database: {Category.objects.count()}")

if __name__ == '__main__':
    create_categories()

