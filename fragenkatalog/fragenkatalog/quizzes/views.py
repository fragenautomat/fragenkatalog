from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone

from fragenkatalog.quizzes.forms import NewQuizForm
from fragenkatalog.quizzes.models import Quiz
from fragenkatalog.responses import reload


@login_required
def my_quizzes(request):
    return TemplateResponse(request, "index.html", {
        "quizzes": Quiz.objects.filter(created_by=request.user),
    })


@login_required
def delete_quiz(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    if request.user != quiz.created_by:
        messages.error(request, "You can only delete your own quizzes!")
        return reload(request)
    if not quiz:
        messages.debug(request, "There is no quiz with the id %s" % id)
        return reload(request)
    quiz.delete()
    messages.success(request, "Quiz was successfully deleted!")
    return reload(request)


@login_required
def new_quiz(request):
    if not request.method == "POST":
        messages.debug(request, "Quiz creation is only allowed via POST.")
        return reload(request)
    form = NewQuizForm(request.POST)
    if not form.is_valid():
        messages.error(request, "The submitted form is incorrect.")
        return reload(request)
    if Quiz.objects.filter(title=form.cleaned_data["title"]).exists():
        messages.warning(request, "A Quiz with the title {} already exists.".format(
            form.cleaned_data["title"]
        ))
        return reload(request)
    quiz = Quiz.objects.create(
        title=form.cleaned_data["title"],
        description=form.cleaned_data["description"],
        created_by=request.user
    )
    messages.success(request, "A new quiz was created!")
    return edit_quiz(request, quiz.id)


@login_required
def edit_quiz(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    if request.user != quiz.created_by:
        messages.error(request, "You can only edit your own quizzes!")
        return reload(request)
    return TemplateResponse(request, "quizzes/edit_quiz.html", {"quiz": quiz})


