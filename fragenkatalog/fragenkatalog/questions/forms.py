from django import forms


class NewQuestionForm(forms.Form):
    description = forms.CharField(label="Description of the task", max_length=10000, required=False)
    solution = forms.CharField(label="Solution of the task", max_length=10000, required=False)
    description_image = forms.ImageField(required=False)
    solution_image = forms.ImageField(required=False)
