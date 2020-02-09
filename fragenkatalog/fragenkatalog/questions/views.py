from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.core.exceptions import ObjectDoesNotExist

from fragenkatalog.questions.forms import NewQuestionForm
from fragenkatalog.questions.models import TextualQuestion, Question
from fragenkatalog.quizzes.models import Quiz
from fragenkatalog.responses import reload
from fragenkatalog.questions.tools import RandomizablePaginator

from fragenkatalog.quizzes.views import edit_quiz

from fragenkatalog.djangostatistics.models import Interaction


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
    if request.user != associated_quiz.created_by:
        messages.error(request, "You can only edit your own quizzes!")
        return reload(request)
    if not associated_quiz:
        messages.error(request, "No associated quiz found.")
        return reload(request)
    TextualQuestion.objects.create(
        description=form.cleaned_data["description"],
        solution=form.cleaned_data["solution"],
        quiz=associated_quiz,
        description_image=form.cleaned_data["description_image"],
        solution_image=form.cleaned_data["solution_image"]
    )
    messages.success(request, "A new textual question was added!")

    Interaction.objects.create(interaction_type="New question added")

    return edit_quiz(request, quiz_id)


@login_required
def edit_question(request, quiz_id, question_id):
    form = NewQuestionForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, "The submitted form is incorrect: {}".format(form.errors))
        return reload(request)
    try:
        question = TextualQuestion.objects.get(id=question_id)
    except ObjectDoesNotExist:
        messages.error(request, "This question is unavailable.")
        return reload(request)
    if question.quiz_id != int(quiz_id):
        messages.error(request, "You can only edit your own quizzes!")
        return reload(request)
    if request.user != question.quiz.created_by:
        messages.error(request, "You can only edit your own quizzes!")
        return reload(request)
    if not request.method == "POST":
        return TemplateResponse(request, "quizzes/edit_quiz.html", {"quiz": question.quiz, "question": question})
    question.description = form.cleaned_data["description"]
    question.solution = form.cleaned_data["solution"]
    if form.cleaned_data["description_image"]:
        question.description_image = form.cleaned_data["description_image"]
    if form.cleaned_data["solution_image"]:
        question.solution_image = form.cleaned_data["solution_image"]
    question.save()
    messages.success(request, "The question was successfully edited!")

    Interaction.objects.create(interaction_type="Question edited")

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

    Interaction.objects.create(
        interaction_type="Questionnaire of quiz \"{}\" visited".format(associated_quiz.title)
    )

    return TemplateResponse(request, "questionnaire.html", {
        "quiz": associated_quiz,
        "questions": questions
    })
