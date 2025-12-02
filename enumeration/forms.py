from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        field
