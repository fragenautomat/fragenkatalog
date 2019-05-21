from django import forms


class NewTextualQuestionForm(forms.Form):
    description = forms.CharField(label="Description of the task", max_length=1000)
    solution = forms.CharField(label="Solution of the task", max_length=1000)
    image = forms.ImageField(required=False)
