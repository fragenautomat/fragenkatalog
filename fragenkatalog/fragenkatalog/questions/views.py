from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from fragenkatalog.questions.forms import NewQuestionForm
from fragenkatalog.questions.models import TextualQuestion, Question, MultipleChoiceQuestion
from fragenkatalog.quizzes.models import Quiz
from fragenkatalog.responses import reload
from fragenkatalog.questions.tools import RandomizablePaginator


@login_required
def new_question(request, quiz_id):
    if not request.method == "POST":
        messages.debug(request, "Question creation is only allowed via POST.")
        return reload(request)
    form = NewQuestionForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, "The submitted form is incorrect: {}".format(form.errors))
        return reload(request)
    associated_quiz = Quiz.objects.get(id=quiz_id)
    if not associated_quiz:
        messages.error(request, "No associated quiz found.")
        return reload(request)
    try:
        MultipleChoiceQuestion.create(
            description=form.cleaned_data["description"],
            solution=form.cleaned_data["solution"],
            quiz=associated_quiz,
            description_image=form.cleaned_data["description_image"],
            solution_image=form.cleaned_data["solution_image"]
        )
        messages.success(request, "A new multiple choice question was added!")
    except ValueError:
        TextualQuestion.objects.create(
            description=form.cleaned_data["description"],
            solution=form.cleaned_data["solution"],
            quiz=associated_quiz,
            description_image=form.cleaned_data["description_image"],
            solution_image=form.cleaned_data["solution_image"]
        )
        messages.success(request, "A new textual question was added!")
    return reload(request)

def questionnaire(request, quiz_id):
    associated_quiz = Quiz.objects.get(id=quiz_id)
    if not associated_quiz:
        messages.error(request, "No associated quiz found.")
        return reload(request)
    questions = associated_quiz.question_set.all()
    question_paginator = RandomizablePaginator(questions, 1)
    question_page = request.GET.get("question")
    questions = question_paginator.get_page(question_page)

    return TemplateResponse(request, "questionnaire.html", {
        "quiz": associated_quiz,
        "questions": questions
    })
