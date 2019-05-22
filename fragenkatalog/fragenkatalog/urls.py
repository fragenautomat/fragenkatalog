"""fragenkatalog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from fragenkatalog import views, settings
from fragenkatalog.quizzes.urls import urls as quizzes_urls
from fragenkatalog.questions.urls import urls as questions_urls

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'i18n/', include('django.conf.urls.i18n')),

    path("accounts/login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(template_name="index.html"), name="logout"),
    url(r'^admin/', admin.site.urls),

    url(r'^quizzes/', include(quizzes_urls)),
    url(r'^questions/', include(questions_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
