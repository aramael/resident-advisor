from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def twilio(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        response = str(func(*args, **kwargs))
        return HttpResponse(response)
    return csrf_exempt(wrapper)