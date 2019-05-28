from django.http import HttpResponseRedirect


def reload(request):
    return HttpResponseRedirect("/")