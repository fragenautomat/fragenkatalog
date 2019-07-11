from django import forms


class NewQuestionForm(forms.Form):
    description = forms.CharField(label="Description of the task", max_length=10000)
    solution = forms.CharField(label="Solution of the task", max_length=10000)
    description_image = forms.ImageField(required=False)
    solution_image = forms.ImageField(required=False)
