from django.contrib import admin

from fragenkatalog.quizzes.models import Quiz, QuizHashTagRelation, HashTag

admin.site.register(Quiz)
admin.site.register(QuizHashTagRelation)
admin.site.register(HashTag)