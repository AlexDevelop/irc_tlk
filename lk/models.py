from django.db import models
from todos.models import TimeStampedModel


class City(TimeStampedModel):
    country = models.CharField(blank=True, null=True, max_length=255)
    city_name = models.CharField(blank=True, null=True, max_length=255)
    connected_cities = models.CharField(blank=True, null=True, max_length=4096)



