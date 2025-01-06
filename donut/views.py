from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.http import JsonResponse
from django.shortcuts import render

from donut.models import Shop


def index(request):
    shops = Shop.objects.order_by("name").all()[:5]
    context = {"shops": shops}
    return render(request, "index.html", context)


def shop_data(request):
    shops = list(Shop.objects.values("name", "review", "lon", "lat"))
    return JsonResponse(shops, safe=False)


def calculate_distances(request):
    lat = float(request.GET.get("lat"))
    lon = float(request.GET.get("lon"))

    # Create a Point object for the clicked location
    clicked_point = Point(lon, lat, srid=4326)

    print(clicked_point)
    shops = Shop.objects.annotate(distance=Distance("point", clicked_point)).order_by(
        "distance"
    )[:5]

    shop_data = [
        {
            "name": shop.name,
            "review": shop.review,
            "lat": shop.lat,
            "lon": shop.lon,
            "distance": shop.distance.m,
            "address_line_1": shop.address_line_1,
        }
        for shop in shops
    ]

    return JsonResponse(shop_data, safe=False)
