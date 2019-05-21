from django.template.response import TemplateResponse

from fragenkatalog.quizzes.models import Quiz


def index(request):
    return TemplateResponse(request, "index.html", {
        "quizzes": Quiz.objects.all()
    })