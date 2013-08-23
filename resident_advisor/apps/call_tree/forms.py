from django import forms
from resident_advisor.libs.forms import ActionMethodForm, HideOwnerForm
from .models import RACallProfile


class RACallProfileForm(ActionMethodForm, HideOwnerForm, forms.ModelForm):

    first_name = forms.CharField()
    last_name = forms.CharField()

    POSSIBLE_ACTIONS = {'_save', }

    class Meta:
        model = RACallProfile
        exclude = ['formatted_phone_number', ]

    def location_redirect(self, action, instance):
        if action == '_save':
            return {"to": 'call_tree_proflie'}