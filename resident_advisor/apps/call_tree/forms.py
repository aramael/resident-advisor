from django import forms
from resident_advisor.libs.forms import ActionMethodForm, HideOwnerForm, FieldsetsForm
from .models import RACallProfile, RACallTree
from .widgets import TwilioPhoneNumberLookup
from twilio.rest import TwilioRestClient
from django.conf import settings
from .helpers import url_with_get

class RACallProfileForm(ActionMethodForm, HideOwnerForm, forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()

    POSSIBLE_ACTIONS = {'_save', }

    class Meta:
        model = RACallProfile
        exclude = ['formatted_phone_number', ]

    def __init__(self, *args, **kwargs):

        super(RACallProfileForm, self).__init__(*args, **kwargs)

        self.initial.update({
            'first_name': self.instance.user.first_name,
            'last_name': self.instance.user.last_name,
        })

    def location_redirect(self, action, instance):
        if action == '_save':
            return {"to": 'call_tree_profile_self'}

    def save(self, *args, **kwargs):

        if self.instance is not None:

            self.instance.user.first_name = self.cleaned_data['first_name']
            self.instance.user.last_name = self.cleaned_data['last_name']
            self.instance.user.save(*args, **kwargs)

        return super(RACallProfileForm, self).save(*args, **kwargs)


class RACallTreeForm(ActionMethodForm, forms.ModelForm, FieldsetsForm):

    fieldsets = (
        (None, {
            'fields': ('nice_name',)
        }),
        ("Phones", {
            'fields': ('call_number', 'phone_numbers',)
        }),
        ("Permissions", {
            'fields': ('owners',)
        }),
    )

    POSSIBLE_ACTIONS = {'_save'}

    class Meta:
        model = RACallTree
        fields = ['nice_name', 'call_number', 'phone_numbers', 'owners']
        widgets = {
            'call_number': TwilioPhoneNumberLookup()
        }

    def save(self, request, commit=True):

        action = self.cleaned_data['action']

        del self.cleaned_data['action']

        instance = super(ActionMethodForm, self).save(commit)

        if commit:
            # Purchase Phone Number
            client = TwilioRestClient(settings.TWILIO_ACCOUNT, settings.TWILIO_TOKEN)
            number = client.phone_numbers.purchase(phone_number=self.cleaned_data['call_number'])
            try:
                number.update(voice_url=url_with_get(request, 'call_tree_receive_call'))
            except AttributeError:
                pass

        location_redirect = self.location_redirect(action, instance)

        return location_redirect

    def location_redirect(self, action, instance):
        if action == '_save':
            return {"to": 'call_tree_view', 'call_tree_id': instance.pk}


class RACallTreeEditForm(ActionMethodForm, FieldsetsForm, forms.ModelForm):

    fieldsets = (
        (None, {
            'fields': ('phone_numbers',)
        }),
    )

    POSSIBLE_ACTIONS = {'_save'}

    class Meta:
        model = RACallTree
        fields = ['phone_numbers',]

    def location_redirect(self, action, instance):
        if action == '_save':
            return {"to": 'call_tree_view', 'call_tree_id': instance.pk}