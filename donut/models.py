from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class Shop(models.Model):
    name = models.CharField(max_length=255)
    review = models.CharField(max_length=255)
    lon = models.FloatField()
    lat = models.FloatField()
    point = models.PointField()

    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.point = Point(self.lon, self.lat, srid=4326)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
