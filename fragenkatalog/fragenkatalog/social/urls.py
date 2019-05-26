from django.conf.urls import url

from fragenkatalog.social import views

urls = [
    url(r'quiz/like/$', views.like_quiz, name='like_quiz'),
    url(r'compilation/like/$', views.like_compilation, name='like_compilation'),
]