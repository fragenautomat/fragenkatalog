from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.http import JsonResponse

from fragenkatalog.language.processing import score

import json


def score_callback(request):
    proposed_text = request.POST.get("proposed_text")
    target_text = request.POST.get("target_text")
    if not proposed_text or not target_text:
        return JsonResponse({"success": json.dumps(False)})

    existing_features, missing_features, achieved_score, achieveable_score = score(
        proposed_text, target_text
    )
    percentage = achieved_score / achieveable_score if achieveable_score != 0 else 0

    print(existing_features, missing_features)

    return JsonResponse({
        "success": True,
        "existing_features": existing_features,
        "missing_features": missing_features,
        "achieved_score": achieved_score,
        "achieveable_score": achieveable_score,
        "percentage": percentage,
    })
