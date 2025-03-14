from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import TestObject, Profile, Class, Item
from django.contrib.auth import logout
from django.core.files.storage import default_storage

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
def home_page_router(request):
    if request.user.profile.userRole == 1:
        return librarian_home_page(request)
    elif request.user.profile.userRole == 0:
        return home_page(request)

@login_required
def home_page(request):
    return render(request, "home_page.html")

@login_required
def librarian_home_page(request):
    return render(request, "librarian_home_page.html")

@login_required
def profile(request):
    return render(request, "profile.html")

def upload_pfp(request):
    if request.method == 'POST' and request.FILES.get('pfp'):
        pfp = request.FILES['pfp']
        file_url = default_storage.save(f"media/profile_pics/{request.user.username}.png", pfp)
    return profile(request)


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

@login_required
def required_materials(request):
    classes = Class.objects.all()
    return render(request, "required_materials.html", {"classes": classes})

@login_required
def class_detail(request, slug):
    class_obj = get_object_or_404(Class, slug=slug)
    required_items = Item.objects.filter(tags__class_obj=class_obj).distinct()
    return render(request, 'class_detail.html', {'class_obj': class_obj, 'required_items': required_items})
