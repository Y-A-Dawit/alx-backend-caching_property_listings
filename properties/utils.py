# properties/utils.py

from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Try fetching from cache first
    properties = cache.get('all_properties')
    
    if not properties:
        # If not cached, query the database
        properties = list(Property.objects.all().values(
            "id", "title", "description", "price", "location", "created_at"
        ))
        # Save to cache for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)
    
    return properties
