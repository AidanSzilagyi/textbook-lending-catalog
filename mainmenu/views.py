from django.shortcuts import render
from django.http import HttpResponse
from .models import TestObject

def index(request):
    info = TestObject.objects.get(pk=1)
    return render(request, "mainmenu/index.html", {"info": info})