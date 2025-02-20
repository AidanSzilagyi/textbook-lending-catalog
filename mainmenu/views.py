from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import TestObject
from django.contrib.auth import logout

def index(request):
    try:
        info = TestObject.objects.get(pk=1)
    except TestObject.DoesNotExist:
        return render(request, "mainmenu/index.html", {"info": "This text only appears locally"})
    return render(request, "mainmenu/index.html", {"info": info.important_text})

def logout_view(request):
    logout(request)
    return redirect("/")


@login_required
def home_page(request):
    return render(request, "home_page.html")