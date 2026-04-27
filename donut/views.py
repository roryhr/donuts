from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.http import JsonResponse
from django.shortcuts import render

from donut.models import Shop


def index(request):
    query_name = request.GET.get("name")
    print("query name", query_name)
    shops = Shop.objects.order_by("name").all()

    if query_name:
        # Search shops whose name contains the query (case-insensitive)
        shops = shops.filter(name__icontains=query_name)
    else:
        # If no query, return top 10 ordered by name (or all, depending on preference)
        shops = Shop.objects.order_by("name")[:10]

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
            "address_line_2": shop.address_line_2,
        }
        for shop in shops
    ]

    return JsonResponse(shop_data, safe=False)


def search_shops(request):
    query = request.GET.get("q")
    if query:
        # Search shops whose name contains the query (case-insensitive)
        shops = Shop.objects.filter(name__icontains=query).order_by("name")
    else:
        shops = Shop.objects.none()

    # Return relevant shop data
    shop_data = [
        {
            "name": shop.name,
            "review": shop.review,
            "lat": shop.lat,
            "lon": shop.lon,
            "distance": None,  # Distance is not calculated here
            "address_line_1": shop.address_line_1,
            "address_line_2": shop.address_line_2,
        }
        for shop in shops
    ]
