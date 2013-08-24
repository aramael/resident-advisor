from django import forms
from resident_advisor.libs.forms import ActionMethodForm, HideOwnerForm
from .models import RACallProfile, RACallTree


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
            return {"to": 'call_tree_proflie'}

    def save(self, *args, **kwargs):

        if self.instance is not None:

            self.instance.user.first_name = self.cleaned_data['first_name']
            self.instance.user.last_name = self.cleaned_data['last_name']
            self.instance.user.save(*args, **kwargs)

        return super(RACallProfileForm, self).save(*args, **kwargs)


class RACallTreeForm(ActionMethodForm, forms.ModelForm):

    POSSIBLE_ACTIONS = {'_save', '_addanother', '_continue'}

    class Meta:
        model = RACallTree

    def location_redirect(self, action, instance):
        if action == '_save':
            return {"to": 'call_tree_home'}
        elif action == '_addanother':
            return {"to": 'call_tree_new'}
        elif action == '_continue':
            return {"to": 'call_tree_view', 'call_tree_id': instance.pk}