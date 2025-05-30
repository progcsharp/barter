from functools import wraps
from django.http import HttpResponse, Http404


def handle_not_found(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Http404:
            return HttpResponse("Объект не найден или больше не доступен.", status=404)
    return wrapper