from .helpers import format_phone_number
from django.db import models
from django.contrib.auth.models import User


class RACallProfile(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length=25)
    formatted_phone_number = models.CharField(max_length=25, blank=True, null=True)

    def save(self, *args, **kwargs):

        self.formatted_phone_number = format_phone_number(self.phone_number)

        super(RACallProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        if hasattr(self.user, 'first_name'):
            return self.user.first_name + ' ' + self.user.last_name
        else:
            return self.user.username


class RACallTree(models.Model):
    owners = models.ManyToManyField(User, null=True, blank=False)
    nice_name = models.CharField(max_length=50)
    phone_numbers = models.ManyToManyField(RACallProfile)
    call_number = models.CharField(max_length=25, blank=True, null=False)

    def display_owners(self):

        owners = self.owners.all()

        display_text = ''

        for owner in owners:
            if hasattr(owner, 'first_name'):
                display_text += owner.first_name + ' ' + owner.last_name + ','
            else:
                display_text += owner.username + ','

        return display_text[:-1]

    def has_change_permissions(self, entity):

        # Active superusers have all permissions.
        if entity.is_active and entity.is_superuser:
            return True

        # Owners of the Tree have all permissions.
        if entity in self.owners.all():
            return True

        return False