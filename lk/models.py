from django.db import models
from todos.models import TimeStampedModel


class City(TimeStampedModel):
    country = models.CharField(blank=True, null=True, max_length=255)
    city_name = models.CharField(blank=True, null=True, max_length=255)
    connected_cities = models.CharField(blank=True, null=True, max_length=4096)
    terrain = models.CharField(blank=True, null=True, max_length=4096)
    type_city = models.CharField(blank=True, null=True, max_length=4096)


class CityToCity(TimeStampedModel):
    city_name_from = models.CharField(blank=True, null=True, max_length=255)
    city_name_to = models.CharField(blank=True, null=True, max_length=255)
    mps = models.IntegerField(default=1)


