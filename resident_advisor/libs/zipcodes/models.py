from django.db import models


class ZipCode(models.Model):
    zipcode = models.CharField(max_length=5, primary_key=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    timezone = models.IntegerField()
    dst = models.BooleanField()
