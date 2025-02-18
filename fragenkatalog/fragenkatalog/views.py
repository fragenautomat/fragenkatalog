from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from fragenkatalog.compilations.models import Compilation
from fragenkatalog.forms import SearchForm, RegistrationForm
from fragenkatalog.quizzes.models import Quiz, HashTag
from fragenkatalog.responses import reload
from fragenkatalog.djangostatistics.models import Interaction


def index(request):
    quizzes = Quiz.objects.all()
    if len(quizzes) > 3:
        quiz_paginator = Paginator(quizzes, 3)
        quiz_page = request.GET.get("quiz_page")
        quizzes = quiz_paginator.get_page(quiz_page)

    compilations = Compilation.objects.all()
    if len(compilations) > 3:
        compilation_paginator = Paginator(compilations, 3)
        compilation_page = request.GET.get("compilation_page")
        compilations = compilation_paginator.get_page(compilation_page)

    Interaction.objects.create(interaction_type="Index page visited")

    return TemplateResponse(request, "index.html", {
        "quizzes": quizzes,
        "compilations": compilations,
    })


def search(request):
    if not request.method == "POST":
        messages.debug(request, "Search is only allowed via POST.")
        return reload(request)
    form = SearchForm(request.POST)
    if not form.is_valid():
        return reload(request)
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

    Interaction.objects.create(interaction_type="Questionnaire searched")

    return TemplateResponse(request, "index.html", {
        "quizzes": quizzes,
        "compilations": compilations,
        "search": form.cleaned_data["search"],
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

    Interaction.objects.create(interaction_type="New user created")

    return TemplateResponse(request, "registration/register.html", {"form": form})
