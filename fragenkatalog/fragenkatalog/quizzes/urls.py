from django.conf.urls import url

from fragenkatalog.quizzes import views

app_name = "quizzes"

urls = [
    url(r'quiz/new/', views.new_quiz, name='new_quiz'),
    url(r'quiz/delete/(?P<id>[-\w]+)/$', views.delete_quiz, name='delete_quiz'),
]