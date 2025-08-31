# properties/utils.py

from django.core.cache import cache
from .models import Property
import logging

# Set up logging
logger = logging.getLogger(__name__)

def get_all_properties():
    properties = cache.get('all_properties')
    
    if not properties:
        properties = list(Property.objects.all().values(
            "id", "title", "description", "price", "location", "created_at"
        ))
        cache.set('all_properties', properties, 3600)
    
    return properties


def get_redis_cache_metrics():
    """
    Retrieves Redis cache metrics: hits, misses, hit ratio
    """
    try:
        # Get the raw Redis client from django-redis
        client = cache.client.get_client(write=True)
        
        # Get Redis INFO
        info = client.info('stats')
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        
        total = hits + misses
        hit_ratio = hits / total if total > 0 else 0
        
        metrics = {
            "keyspace_hits": hits,
            "keyspace_misses": misses,
            "hit_ratio": round(hit_ratio, 2)
        }
        
        # Log metrics
        logger.info(f"Redis Cache Metrics: {metrics}")
        
        return metrics
    
    except Exception as e:
        logger.error(f"Error fetching Redis metrics: {e}")
        return {"keyspace_hits": 0, "keyspace_misses": 0, "hit_ratio": 0}
