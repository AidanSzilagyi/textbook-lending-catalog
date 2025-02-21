from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import TestObject, Profile
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

@login_required
def librarian_home_page(request, account_user):
    i
    return render(request, "librarian_home_page.html")

@login_required
def profile(request):
    return render(request, "profile.html")

@login_required
def messaging(request):
    return render(request, "messaging.html")

@login_required
def lent_items(request):
    return render(request, "lent_items.html")

@login_required
def borrowed_items(request):
    return render(request, "borrowed_items.html")

@login_required
def marketplace(request):
    return render(request, "marketplace.html")