from django import forms


class NewQuizForm(forms.Form):
    title = forms.CharField(label="Quiz Title", max_length=100)
    description = forms.CharField(label="Quiz Description")
    image = forms.ImageField(required=False)
