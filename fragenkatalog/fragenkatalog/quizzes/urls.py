from django.conf.urls import url

from fragenkatalog.quizzes import views

urls = [
    url(r'quiz/my/', views.my_quizzes, name='my_quizzes'),
    url(r'quiz/edit/(?P<id>[-\w]+)', views.edit_quiz, name='edit_quiz'),
    url(r'quiz/new/', views.new_quiz, name='new_quiz'),
    url(r'quiz/delete/(?P<id>[-\w]+)/$', views.delete_quiz, name='delete_quiz'),
]