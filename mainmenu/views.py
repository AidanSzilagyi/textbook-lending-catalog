from django.contrib.auth.decorators import login_required
from django.contrib.messages.storage import default_storage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template.defaultfilters import slugify
from .forms import ItemForm, CollectionForm
from .models import TestObject, Profile, Item, Class, Tag, ItemImage, NewCollection
from django.contrib.auth import logout
from django.template import loader
from django.urls import reverse
from django.core.files.storage import default_storage
from .models import NewCollection, CollectionAccessRequest

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
    if request.user.is_authenticated:
        if request.user.profile.userRole == 0:
            return home_page(request)
        elif request.user.profile.userRole == 1:
            return librarian_home_page(request)
    return unauth_home_page(request)

def unauth_home_page(request):
    return render(request, 'unauth_home.html')

@login_required
def home_page(request):
    context = {
        'tags': Tag.objects.all(),
        'items': Item.objects.all(),
    }
    return render(request, 'home_page.html', context)

@login_required
def librarian_home_page(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            for f in request.FILES.getlist('images'):
                img = ItemImage.objects.create(image=f)
                item.images.add(img)
            return redirect('librarian_home_page')
    else:
        form = ItemForm()

    items = Item.objects.all().order_by('-id')

    return render(request, "librarian_home_page.html", {
        'form': form,
        'items': items,
    })

@login_required
def profile(request):
    return render(request, "profile.html")

@login_required
def upload_pfp(request):
    if request.method == 'POST' and request.FILES.get('pfp'):
        profile = request.user.profile
        profile.profile_picture = request.FILES['pfp']
        profile.save()
    return redirect('/profile/')

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


def class_detail(request, slug):
    class_obj = get_object_or_404(Class, slug=slug)
    required_tags = class_obj.required_tags.all()
    available_tags = Tag.objects.exclude(id__in=required_tags.values_list('id', flat=True))

    context = {
        'class_obj': class_obj,
        'required_tags': required_tags,
        'available_tags': available_tags,
    }
    return render(request, 'class_detail.html', context)

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
def class_create(request):
    if request.user.profile.userRole != 1:
        return HttpResponseForbidden("You are not authorized to add a class.")

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")

        if not name or not description:
            return redirect('home_page')

        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        while Class.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        new_class = Class.objects.create(name=name, description=description, slug=slug)

        return redirect('class_detail', slug=new_class.slug)

    return redirect('home_page')


@login_required
def tag_create(request):
    if request.user.profile.userRole != 1:
        return HttpResponseForbidden("You are not authorized to add a tag.")

    if request.method == "POST":
        tag_name = request.POST.get("tag_name", "").strip()
        if tag_name:
            Tag.objects.create(name=tag_name)
        return redirect('librarian_home_page')

    return redirect('librarian_home_page')

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


@login_required
def material_create(request, slug):
    if request.user.profile.userRole != 1:
        return HttpResponseForbidden("You are not authorized to add material.")

    class_obj = get_object_or_404(Class, slug=slug)

    if request.method == "POST":
        identifier = request.POST.get("identifier", "").strip()
        is_available = request.POST.get("is_available") == "on"
        tag_ids = request.POST.getlist("tags")

        new_item = Item.objects.create(identifier=identifier, is_available=is_available)

        if tag_ids:
            valid_tags = Tag.objects.filter(id__in=tag_ids)
            new_item.tags.add(*valid_tags)
        class_obj.items.add(new_item)

        return redirect('class_detail', slug=slug)

    return redirect('class_detail', slug=slug)


@login_required
def unlink_required_tag(request, slug, tag_id):
    if request.user.profile.userRole != 1:
        return HttpResponseForbidden("You are not authorized to remove a required tag.")

    class_obj = get_object_or_404(Class, slug=slug)
    tag = get_object_or_404(Tag, id=tag_id)
    class_obj.required_tags.remove(tag)
    return redirect('class_detail', slug=slug)


@login_required
def add_required_tag(request, slug):
    if request.user.profile.userRole != 1:
        return HttpResponseForbidden("You are not authorized to add a required tag.")

    class_obj = get_object_or_404(Class, slug=slug)

    if request.method == "POST":
        tag_id = request.POST.get("tag_id")
        if tag_id:
            tag = get_object_or_404(Tag, id=tag_id)
            class_obj.required_tags.add(tag)
        return redirect('class_detail', slug=slug)

    return redirect('class_detail', slug=slug)


@login_required
def item_post(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            for f in request.FILES.getlist('images'):
                img = ItemImage.objects.create(image=f)
                item.images.add(img)
            return redirect('librarian_home_page')
    else:
        form = ItemForm()
    return render(request, 'librarian_home_page.html', {
        'form': form
    })

@login_required
def item_detail(request, uuid):
    item = get_object_or_404(Item, uuid=uuid)
    return render(request, 'item_detail.html', {
        'item': item
    })

def collection(request):

    if request.method == "POST":
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.creator = request.user.profile  # Assign logged-in user as creator
            collection.save()
            form.save_m2m()  # Save ManyToMany relationships
            return render(request, "collection.html", {'form': form, 'collections': collection}) # Redirect to homepage after submission

    else:
        form = CollectionForm()

    collections = NewCollection.objects.all()
    # user_collections = NewCollection.objects.filter(creator =request.user.profile)

    return render(request, 'collection.html', {'form': form, 'collections': collections, 'user_collections': user_collections})

def collection_detail(request, collection_id):
    collection = get_object_or_404(NewCollection, pk=collection_id)
    items = collection.items.all()  # if you have a related_name like 'items' in FK
    return render(request, 'collection_detail.html', {
        'collection': collection,
        'items': items,
    })

def edit_collection(request, collection_id):
    collection = get_object_or_404(NewCollection, pk=collection_id)

    if request.method == 'POST':
        form = CollectionForm(request.POST, instance=collection)
        if form.is_valid():
            form.save()
            return redirect('collection_detail', collection_id=collection.id)
    else:
        form = CollectionForm(instance=collection)

    return render(request, 'collection_detail.html', {'form': form, 'collection': collection})

@login_required
def request_access(request, collection_id):
    collection = get_object_or_404(NewCollection, pk=collection_id)
    CollectionAccessRequest.objects.get_or_create(user=request.user, collection=collection)
    return redirect('collection_detail', collection_id=collection.id)
