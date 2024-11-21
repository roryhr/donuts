import json

from django.http import JsonResponse
from django.shortcuts import render

from donut.models import Shop


def index(request):
    # shops = Shop.objects.all().values("name", "review", "lon", "lat")
    shops = [
        {"name": "Shop1", "review": "Great shop", "lon": -0.1257, "lat": 51.5085},
        {"name": "Shop2", "review": "Nice place", "lon": -0.142, "lat": 51.5098},
    ]

    shops_json = json.dumps(shops)
    print(shops_json)
    context = {"shops_json": shops_json}
    return render(request, "index.html")


def shop_data(request):
    shops = list(Shop.objects.values("name", "review", "lon", "lat"))
    return JsonResponse(shops, safe=False)
