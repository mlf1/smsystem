# oscm_app/sign

from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _

from oscm_app.custom_auth_user import CustomAuthUser


class LoginForm(forms.Form):
    model = CustomAuthUser
    # username = forms.CharField(max_length=255, required=True)
    # password = forms.CharField(widget=forms.PasswordInput, required=True)
    fields = ('username', 'password')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError(
                _("Sorry, that login was invalid. Please try again."))
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user
