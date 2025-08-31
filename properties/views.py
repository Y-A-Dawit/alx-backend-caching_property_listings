from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from django.views.decorators.cache import cache_page
from .models import Property

@cache_page(60 * 15)  # cache for 15 minutes
def property_list(request):
    properties = Property.objects.all().values(
        "id", "title", "description", "price", "location", "created_at"
    )
    data = list(properties)  # convert QuerySet to list
    return JsonResponse({"data": data})