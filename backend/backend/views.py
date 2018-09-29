from django.http import HttpResponse


def hi(request):
    return HttpResponse("Hi man!")


def index(request):
    return HttpResponse("Base page for the project!")
