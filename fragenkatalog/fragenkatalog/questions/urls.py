from django.conf.urls import url

from fragenkatalog.questions import views

urls = [
    url(r'questions/(?P<quiz_id>[-\w]+)/new/', views.new_question, name='new_question'),
    url(r'questions/(?P<quiz_id>[-\w]+)/edit/(?P<question_id>[-\w]+)', views.edit_question, name='edit_question'),
    url(r'questions/(?P<quiz_id>[-\w]+)/', views.questionnaire, name='questionnaire'),
]
