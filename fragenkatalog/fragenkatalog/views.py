from django.contrib import messages
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from fragenkatalog.forms import SearchForm
from fragenkatalog.quizzes.models import Quiz


def index(request):
    return TemplateResponse(request, "index.html", {
        "quizzes": Quiz.objects.all(),
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
    quizzes = (title_quizzes | description_quizzes).distinct()
    return TemplateResponse(request, "index.html", {
        "quizzes": quizzes,
        "search": form.cleaned_data["search"]
    })