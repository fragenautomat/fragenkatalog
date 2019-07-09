from django.conf.urls import url

from fragenkatalog.language import views

urls = [
    url(r'score-callback/', views.score_callback, name='score_callback'),
]
