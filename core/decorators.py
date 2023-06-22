from functools import wraps

from django.http import HttpResponseForbidden


def ajax_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if request.headers.get('x-requested-with') != 'XMLHttpRequest':
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)

    return wrapped_view
