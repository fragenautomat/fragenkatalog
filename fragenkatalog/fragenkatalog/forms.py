from django import forms
import django.contrib.auth.forms as auth_forms
from django.contrib.auth.models import User


class SearchForm(forms.Form):
    search = forms.CharField(label="Search", max_length=100)


class RegistrationForm(auth_forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'
