from django.db import models
from django.contrib.auth.models import User


class RACallProfile(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length=25)
