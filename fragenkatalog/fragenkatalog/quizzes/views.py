from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone

from fragenkatalog.quizzes.forms import NewQuizForm
from fragenkatalog.quizzes.models import Quiz


@login_required
def delete_quiz(request, id):
    if not request.user or not request.user.is_superuser:
        messages.error(request, "To delete a quiz, you need to be logged in as admin.")
        return HttpResponseRedirect("/")
    quiz = get_object_or_404(Quiz, id=id)
    if not quiz:
        messages.debug(request, "There is no quiz with the id %s" % id)
        return HttpResponseRedirect("/")
    quiz.delete()
    messages.success(request, "Quiz was successfully deleted!")
    return HttpResponseRedirect("/")

@login_required
def new_quiz(request):
    if not request.user.is_superuser:
        messages.error(request, "To create a new quiz, you need to be logged in as admin.")
        return HttpResponseRedirect("/")
    if not request.method == "POST":
        messages.debug(request, "Quiz creation is only allowed via POST.")
        return HttpResponseRedirect("/")
    form = NewQuizForm(request.POST)
    if not form.is_valid():
        messages.error(request, "The submitted form is incorrect.")
        return HttpResponseRedirect("/")
    Quiz.objects.create(
        title=form.cleaned_data["title"],
        description=form.cleaned_data["description"],
        pubdate=timezone.now()
    )
    messages.success(request, "A new quiz was created!")
    return HttpResponseRedirect("/")
