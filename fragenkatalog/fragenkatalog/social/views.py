from django.contrib.auth.decorators import login_required
from django.db.transaction import atomic
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404

from fragenkatalog.compilations.models import Compilation
from fragenkatalog.quizzes.models import Quiz
from fragenkatalog.social.models import Like


@login_required
def like_quiz(request):
    if request.method != "POST":
        return HttpResponseNotFound()
    quiz_id = request.POST.get("quiz_id")
    if not quiz_id:
        return HttpResponseNotFound()
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if quiz.liked_by(request.user):
        return JsonResponse({"success": False})
    with atomic():
        Like.objects.create(
            created_by=request.user,
            content_object=quiz
        )
    return JsonResponse({"success": True})


@login_required
def like_compilation(request):
    if request.method != "POST":
        return HttpResponseNotFound()
    compilation_id = request.POST.get("compilation_id")
    if not compilation_id:
        return HttpResponseNotFound()
    compilation = get_object_or_404(Compilation, id=compilation_id)
    if compilation.liked_by(request.user):
        return JsonResponse({"success": False})
    with atomic():
        Like.objects.create(
            created_by=request.user,
            content_object=compilation
        )
    return JsonResponse({"success": True})
