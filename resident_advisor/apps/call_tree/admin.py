from django.contrib import admin
from django import forms
from django.forms.util import flatatt
from django.template import loader
from django.utils.datastructures import SortedDict
from django.utils.html import format_html, format_html_join
from django.utils.http import int_to_base36
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import UNUSABLE_PASSWORD, identify_hasher
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.core.mail import send_mail


class UserAdmin(UserAdmin):
    """
    Define a new UserAdmin Class to override the django default
    """
    actions = ['resend_activation_email']

    def resend_activation_email(self, request, queryset):
        """
        Re-sends activation emails for the selected users.

        Note that this will *only* send activation emails for users
        who are eligible to activate; emails will not be sent to users
        whose activation keys have expired or who have already
        activated.

        """

        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain

        for user in queryset:

            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.pk),
                'user': user,
                'token': default_token_generator.make_token(user),
                'protocol': request.is_secure(),
            }
            subject = loader.render_to_string('call_tree/password_reset_subject.txt', c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string('call_tree/password_reset_email.html', c)
            send_mail(subject, email, None, [user.email])

    resend_activation_email.short_description = "Re-send activation emails"

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)