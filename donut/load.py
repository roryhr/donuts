"""
To get GDAL working use the Django shell

$ python manage.py shell

In [1]: %run donut/load.py
"""

import json
from pathlib import Path

from donut.models import Shop

data_path = Path("donut/static/map_data.json")

data_json = json.loads(data_path.read_text())["features"]

for shop in data_json:
    coordinates = shop["geometry"]["coordinates"]
    description = shop["properties"]["description"]
    popup_content = shop["properties"]["popupContent"]
    parts = description.split("\n")

    if len(parts) != 5:
        print("Problem with this", parts)
        continue

    [_, address_line_1, address_line_2, _, review] = parts
    print(address_line_1)
    print(address_line_2)
    print(review)

    shop, created = Shop.objects.get_or_create(
        name=popup_content,
        review=description,
        lon=coordinates[0],
        lat=coordinates[1],
    )

    shop.address_line_1 = address_line_1
    shop.address_line_2 = address_line_2
    shop.review = review
    shop.save()
