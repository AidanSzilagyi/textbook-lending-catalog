from django.contrib.auth.decorators import login_required
from django.contrib.messages.storage import default_storage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import TestObject, Profile, Item, Class, Tag
from django.contrib.auth import logout
from django.template import loader
from django.urls import reverse
from django.core.files.storage import default_storage

def index(request):
    try:
        info = TestObject.objects.get(pk=1)
    except TestObject.DoesNotExist:
        return render(request, "mainmenu/index.html", {"info": "This text only appears locally"})
    return render(request, "mainmenu/index.html", {"info": info.important_text})

def logout_view(request):
    logout(request)
    return redirect("index")


def home_page_router(request):
    if not request.user.is_authenticated:
        return home_page(request)
    elif request.user.profile.userRole == 1:
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
        profile = request.user.profile
        profile.profile_picture = request.FILES['pfp']
        profile.save()
    return redirect('profile')

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
    items = Item.objects.all()
    return render(request, "marketplace.html", {"items": items})

@login_required
def librarian_settings(request):
    patron_list = Profile.objects.filter(userRole=0)

    context = {
        "patron_list": patron_list,
    }
    return render(request, "librarian_settings.html", context )

@login_required
def class_detail(request, slug):
    class_obj = get_object_or_404(Class, slug=slug)
    required_items = Item.objects.filter(tags__class_obj=class_obj).distinct()
    return render(request, 'class_detail.html', {'class_obj': class_obj, 'required_items': required_items})

def patron_to_librarian(request):
    patron_list = Profile.objects.filter(userRole=0)
    try:
        selected_patron = patron_list.get(pk=request.POST["patron"])
    except (KeyError, Profile.DoesNotExist):
        return render(request, "librarian_settings.html", {"patron_list": patron_list})
    else:
        selected_patron.userRole = 1
        selected_patron.save()
        return HttpResponseRedirect(reverse("home_page_router"))

@login_required
def required_materials(request):
    classes = Class.objects.all()
    return render(request, "required_materials.html", {"classes": classes})

@login_required
def add_item(request):
    if request.user.profile.userRole != 1:
        return redirect('marketplace')
    
    classes = Class.objects.all()
    tags = Tag.objects.all()
    
    return render(request, "add_item.html", {
        "classes": classes,
        "tags": tags
    })

@login_required
def add_item_submit(request):
    if request.user.profile.userRole != 1:
        return redirect('marketplace')
    
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        is_available = 'is_available' in request.POST
        
        new_item = Item(
            identifier=identifier,
            is_available=is_available
        )
        new_item.save()
        
        tag_ids = request.POST.getlist('tags')
        for tag_id in tag_ids:
            tag = Tag.objects.get(id=tag_id)
            new_item.tags.add(tag)
        
        if request.FILES.get('item_pic'):
            item_pic = request.FILES['item_pic']
            clean_name = ''.join(c for c in identifier if c.isalnum() or c in '._- ')
            clean_name = clean_name.replace(' ', '_').lower()
            file_url = default_storage.save(f"media/item_pics/{clean_name}.png", item_pic)        
        return redirect('marketplace')
    
    return redirect('add_item')
