from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "mainmenu/index.html", dict())
    # HttpResponse("Welcome to the main menu.")