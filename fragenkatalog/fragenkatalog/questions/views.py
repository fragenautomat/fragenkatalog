from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from fragenkatalog.questions.forms import NewTextualQuestionForm
from fragenkatalog.questions.models import TextualQuestion
from fragenkatalog.quizzes.models import Quiz


@login_required
def new_question(request, quiz_id):
    if not request.user.is_superuser:
        messages.error(request, "To create a new question, you need to be logged in as admin.")
        return HttpResponseRedirect("/")
    if not request.method == "POST":
        messages.debug(request, "Question creation is only allowed via POST.")
        return HttpResponseRedirect("/")
    form = NewTextualQuestionForm(request.POST, request.FILES)
    if not form.is_valid():
        print(form.errors)
        messages.error(request, "The submitted form is incorrect.")
        return HttpResponseRedirect("/")
    associated_quiz = Quiz.objects.get(id=quiz_id)
    if not associated_quiz:
        messages.error(request, "No associated quiz found.")
        return HttpResponseRedirect("/")
    print(form.cleaned_data["image"])
    TextualQuestion.objects.create(
        description=form.cleaned_data["description"],
        solution=form.cleaned_data["solution"],
        quiz=associated_quiz,
        image=form.cleaned_data["image"]
    )
    messages.success(request, "A new question was added!")
    return HttpResponseRedirect("/")

def questionnaire(request, quiz_id):
    associated_quiz = Quiz.objects.get(id=quiz_id)
    if not associated_quiz:
        messages.error(request, "No associated quiz found.")
        return HttpResponseRedirect("/")
    questions = associated_quiz.question_set.all()
    question_paginator = Paginator(questions, 1)
    question_page = request.GET.get("question")
    questions = question_paginator.get_page(question_page)

    return TemplateResponse(request, "questionnaire.html", {
        "quiz": associated_quiz,
        "questions": questions
    })