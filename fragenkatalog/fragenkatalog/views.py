from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from fragenkatalog.compilations.models import Compilation
from fragenkatalog.forms import SearchForm, RegistrationForm
from fragenkatalog.quizzes.models import Quiz, HashTag


def index(request):
    return TemplateResponse(request, "index.html", {
        "quizzes": Quiz.objects.all(),
        "compilations": Compilation.objects.all()
    })


def search(request):
    if not request.method == "POST":
        messages.debug(request, "Search is only allowed via POST.")
        return HttpResponseRedirect("/")
    form = SearchForm(request.POST)
    if not form.is_valid():
        return HttpResponseRedirect("/")
    query = form.cleaned_data["search"]
    if not query:
        return index(request)
    title_quizzes = Quiz.objects.filter(title__icontains=query)
    description_quizzes = Quiz.objects.filter(description__icontains=query)
    quizzes = set((title_quizzes | description_quizzes).distinct())
    hashtags = HashTag.objects.filter(title__icontains=query)
    for hashtag in hashtags:
        quizzes.update(hashtag.quiz_set)

    title_compilations = Compilation.objects.filter(title__icontains=query)
    description_compilations = Compilation.objects.filter(description__icontains=query)
    compilations = set(title_compilations | description_compilations)

    return TemplateResponse(request, "index.html", {
        "quizzes": quizzes,
        "compilations": compilations,
        "search": form.cleaned_data["search"]
    })


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Your account was successfully created!")
            return HttpResponseRedirect("/")
    else:
        form = RegistrationForm()
    return TemplateResponse(request, "registration/register.html", {"form": form})