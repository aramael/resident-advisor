from django import forms
from resident_advisor.libs.forms import ActionMethodForm, HideOwnerForm
from .models import RACallProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.utils.datastructures import SortedDict
from django.forms.forms import BoundField


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


class UserCreationForm(ActionMethodForm, forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    POSSIBLE_ACTIONS = {'_save', '_addanother', '_continue'}

    error_messages = {
        'duplicate_username': "A user with that username already exists.",
        'password_mismatch': "The two password fields didn't match.",
    }
    username = forms.RegexField(label="Columbia UNI", max_length=30,
                                regex=r'^[\w.@+-]+$',
                                help_text="Required. 30 characters or fewer. Letters, digits and "
                                          "@/./+/-/_ only.",
                                error_messages={
                                    'invalid': "This value may contain only letters, numbers and "
                                               "@/./+/-/_ characters."})

    first_name = forms.CharField()
    last_name = forms.CharField()

    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput,
                                help_text="Enter the same password as above, for verification.")

    class Meta:
        model = User
        fields = ('username', )

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):

        data = self.cleaned_data

        user = User.objects.create_user(username=data['username'])

        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["username"] + "@columbia.edu"

        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        location_redirect = self.location_redirect(data['action'], user)

        return location_redirect

    def location_redirect(self, action, instance):
        if action == '_save':
            return {"to": 'users_home'}
        elif action == '_addanother':
            return {"to": 'users_new'}
        elif action == '_continue':
            return {"to": 'users_edit', 'user_id': instance.pk}


class UserEditForm(ActionMethodForm, UserChangeForm):

    # exclude_fields = ['is_staff', 'date_joined', 'last_login']

    fieldsets = (
        (None, {
            'fields': ('username', 'password',)
        }),
        ("Information", {
            'fields': ('first_name', 'last_name', 'email',)
        }),
        ("Permissions", {
            'fields': ('groups', 'user_permissions',)
        }),
    )

    @property
    def formatted_fieldset(self):

        if not hasattr(self, '_formatted_fieldset'):

            fieldsets = self.fieldsets

            formatted_fieldsets = []

            for fieldset in fieldsets:

                formatted_fieldset = {
                    'title': fieldset[0],
                    'classes': fieldset[1].get('classes', None),
                }

                fields = SortedDict()

                for field in fieldset[1].get('fields', []):
                    field_cls = self.fields.get(field, None)

                    fields[field] = BoundField(form=self, field=field_cls, name=field)

                formatted_fieldset['fields'] = fields

                formatted_fieldsets.append(formatted_fieldset)

            self._formatted_fieldset = formatted_fieldsets

        return self._formatted_fieldset

    def location_redirect(self, action, instance):
        if action == '_save':
            return {"to": 'users_home'}
        elif action == '_addanother':
            return {"to": 'users_new'}
        elif action == '_continue':
            return {"to": 'users_edit', 'user_id': instance.pk}