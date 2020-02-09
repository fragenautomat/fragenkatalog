from django.conf.urls import url

from fragenkatalog.questions import views

urls = [
    url(r'quiz/(?P<quiz_id>[-\w]+)/questions/new/', views.new_question, name='new_question'),
    url(r'quiz/(?P<quiz_id>[-\w]+)/questions/(?P<question_id>[-\w]+)/edit/', views.edit_question, name='edit_question'),
    url(r'quiz/(?P<quiz_id>[-\w]+)/$', views.questionnaire, name='questionnaire'),
    url(r'quiz/(?P<quiz_id>[-\w]+)/all/', views.questionnaire_all, name='questionnaire_all'),
]
