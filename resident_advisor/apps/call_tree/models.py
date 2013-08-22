from .helpers import format_phone_number
from django.db import models
from django.contrib.auth.models import User


class RACallProfile(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length=25)
    formatted_phone_number = models.CharField(max_length=25, blank=True, null=False)

    def save(self, *args, **kwargs):

        self.formatted_phone_number = format_phone_number(self.phone_number)

        super(RACallProfile,self).save(*args, **kwargs)