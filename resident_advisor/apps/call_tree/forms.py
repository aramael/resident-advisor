from django import forms
from resident_advisor.libs.forms import ActionMethodForm
from .models import RACallProfile


class RACallProfileForm(ActionMethodForm, forms.ModelForm):

    POSSIBLE_ACTIONS = {'_save', }

    class Meta:
        model = RACallProfile

    def location_redirect(self, action, instance):
        if action == '_save':
            return {"to": 'call_tree_proflie'}