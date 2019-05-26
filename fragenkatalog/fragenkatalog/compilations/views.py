from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse

from fragenkatalog.compilations.models import Compilation
from fragenkatalog.quizzes.models import Quiz


def compilation(request, compilation_id):
    associated_compilation = get_object_or_404(Compilation, id=compilation_id)
    return TemplateResponse(request, "compilation.html", {
        "compilation": associated_compilation,
        "quizzes": Quiz.objects.filter(compilation_id=compilation_id)
    })
