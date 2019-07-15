from django.contrib import admin

from fragenkatalog.questions.models import TextualQuestion, Question

admin.site.register(TextualQuestion)
admin.site.register(Question)
