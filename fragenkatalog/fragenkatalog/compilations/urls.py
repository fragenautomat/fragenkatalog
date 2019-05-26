from django.conf.urls import url

from fragenkatalog.compilations import views

urls = [
    url(r'compilation/(?P<compilation_id>[-\w]+)/', views.compilation, name='compilation'),
]