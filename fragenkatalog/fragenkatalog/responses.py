from django.http import HttpResponseRedirect


def reload(request):
    if request.META.get("HTTP_REFERER"):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return HttpResponseRedirect("/")