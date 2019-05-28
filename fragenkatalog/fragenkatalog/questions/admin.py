from django.contrib import admin

from fragenkatalog.questions.models import TextualQuestion, Question, MultipleChoiceQuestion, MultipleChoiceOption

admin.site.register(TextualQuestion)
admin.site.register(Question)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(MultipleChoiceOption)