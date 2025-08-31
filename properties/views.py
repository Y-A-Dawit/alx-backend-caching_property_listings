from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property
from .utils import get_all_properties, get_redis_cache_metrics

@cache_page(60 * 15)  # cache for 15 minutes
def property_list(request):
    properties = get_all_properties()
    return JsonResponse({"data": properties})

metrics = get_redis_cache_metrics()
print(metrics)