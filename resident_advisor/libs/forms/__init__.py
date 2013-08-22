from django import forms


class ActionMethodForm(object):

    POSSIBLE_ACTIONS = None

    def clean(self):
        cleaned_data = super(ActionMethodForm, self).clean()

        # Check For Form Action
        if not self.POSSIBLE_ACTIONS.isdisjoint(cleaned_data):
            raise forms.ValidationError(
                'Invalid Action',
                code='invalid-action',
            )

        # Determine Form Action

        action = list(self.POSSIBLE_ACTIONS & set(self.data))

        if len(action) != 1:
            raise forms.ValidationError(
                'Multiple Actions Detected. Please Try Again',
                code='invalid-action',
            )

        cleaned_data['action'] = action[0]

        return cleaned_data

    def save(self, commit=True):

        action = self.cleaned_data['action']

        del self.cleaned_data['action']

        instance = super(ActionMethodForm, self).save(commit)

        location_redirect = self.location_redirect(action, instance)

        return location_redirect

    def location_redirect(self, action, instance):

        raise NotImplementedError


class HideOwnerForm(object):

    def __init__(self, *args, **kwargs):
        super(HideOwnerForm, self).__init__(*args, **kwargs)

        self.fields['owner'].widget = forms.HiddenInput()