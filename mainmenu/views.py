from django.contrib.auth.decorators import login_required
from django.contrib.messages.storage import default_storage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template.defaultfilters import slugify
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .forms import ProfileForm

from .forms import ItemForm, CollectionForm
from .models import *
from django.contrib.auth import logout
from django.template import loader
from django.urls import reverse
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Notification, Collection, CollectionAccessRequest
from .serializers import NotificationSerializer

# New view: the landing login page
def login_page(request):
    return render(request, "login.html")

def index(request):
    try:
        info = TestObject.objects.get(pk=1)
    except TestObject.DoesNotExist:
        return render(request, "mainmenu/index.html", {"info": "This text only appears locally"})
    return render(request, "mainmenu/index.html", {"info": info.important_text})    

# Update logout_view: after logout, redirect to the new login page
def logout_view(request):
    logout(request)
    return redirect("login_page")

def home_page_router(request):
    print("In home_page_router")
    if request.user.is_authenticated:
        print(f"User is authenticated, role: {request.user.profile.userRole}")
        if request.user.profile.userRole == 0:
            print("Rendering home_page.html")
            return home_page(request)
        elif request.user.profile.userRole == 1:
            print("Rendering librarian_home_page.html")
            return librarian_home_page(request)
    print("User not authenticated, rendering unauth_home.html")
    return unauth_home_page(request)

def unauth_home_page(request):
    """
    For anonymous users, return items that are either:
      - Not in any collection, OR
      - In collections that are all public.
    This is achieved by excluding any item that appears in any collection with visibility set to 'private'.
    """
    q = request.GET.get('q', '')
    # Exclude items that are in any private collections.
    base_items = Item.objects.exclude(collections_of__visibility='private').distinct()
    
    if q:
        items = base_items.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(location__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct().order_by('-id')
    else:
        items = base_items.order_by('-id')
    
    context = {
        'items': items,
        'q': q,
    }
    return render(request, 'unauth_home.html', context)

@login_required
def home_page(request):
    print("In home_page, rendering home_page.html")
    q = request.GET.get('q', '')
    if q:
        items = Item.objects.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(location__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct().order_by('-id')
    else:
        items = Item.objects.all().order_by('-id')

    context = {
        'tags': Tag.objects.all(),
        'items': items,
        'q': q,
    }
    return render(request, 'home_page.html', context)

@login_required
def librarian_home_page(request):
    print("In librarian_home_page, rendering librarian_home_page.html")
    # Handle POST for item submission
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

    # Retrieve the query string from the GET parameters (if any)
    q = request.GET.get('q', '')
    if q:
        # Filter items by matching title, description, location or associated tag names
        items = Item.objects.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(location__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct().order_by('-id')
    else:
        items = Item.objects.all().order_by('-id')

    return render(request, "librarian_home_page.html", {
        'form': form,
        'items': items,
        'q': q,
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
    received = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    sent = Message.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'messaging.html', {'received': received, 'sent': sent})

@login_required
def lent_items(request):
    return render(request, "lent_items.html")

@login_required
def borrowed_items(request):
    available_items = Item.objects.filter(status='available')
    requested_items = Item.objects.filter(status='requested')
    context ={
        'available_items': available_items,
        'requested_items': requested_items,
    }
    return render(request, "borrowed_items.html", context)

def available_to_requested(request):
    available_items = Item.objects.filter(status='available')
    try:
        selected_item = available_items.get(pk=request.POST['item'])
    except (KeyError, Item.DoesNotExist):
        return render(request, "borrowed_items.html", {"available_items": available_items})
    else:
        selected_item.status = 'requested'
        selected_item.save()

        Message.objects.create(
            sender=request.user,
            recipient=selected_item.owner,
            item=selected_item,
            content=f"{request.user.username} has requested to borrow your textbook: {selected_item.title}"
        )

        return HttpResponseRedirect(reverse('home_page_router'))

#https://stackoverflow.com/questions/866272/how-can-i-build-multiple-submit-buttons-django-form
@login_required
def requested_to_in_circulation(request):
    requested_items = Item.objects.filter(status='requested')
    try:
        selected_item = requested_items.get(pk=request.POST['item'])
    except (KeyError, Item.DoesNotExist):
        return render(request, "borrowed_items.html", {"requested_items": requested_items})
    else:
        if 'yes' in request.POST:
            selected_item.status = 'in_circulation'
            selected_item.borrower = selected_item.message_set.filter(item=selected_item).last().sender  # 👈 Patron
            selected_item.save()

            patron = selected_item.borrower

            Message.objects.create(
                sender=request.user,  # owner
                recipient=patron,
                item=selected_item,
                content=f"Your request to borrow '{selected_item.title}' has been accepted. You now have it in circulation!"
            )

            return HttpResponseRedirect(reverse('home_page_router'))

        elif 'no' in request.POST:
            selected_item.status = 'available'
            selected_item.save()

            patron_message = selected_item.message_set.filter(item=selected_item).last()
            if patron_message:
                Message.objects.create(
                    sender=request.user,  # owner
                    recipient=patron_message.sender,
                    item=selected_item,
                    content=f"Your request to borrow '{selected_item.title}' has been denied. The item is now available again."
                )

            return HttpResponseRedirect(reverse('home_page_router'))

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
        title = request.POST.get('title')
        status = request.POST.get('status')
        location = request.POST.get('location', '')
        description = request.POST.get('description', '')

        new_item = Item(
            title=title,
            status=status,
            location=location,
            description=description,
            owner=request.user
        )
        new_item.save()
        tag_ids = request.POST.getlist('tags')
        for tag_id in tag_ids:
            tag = Tag.objects.get(id=tag_id)
            new_item.tags.add(tag)
        images = request.FILES.getlist('images')
        for img in images:
            item_image = ItemImage(image=img)
            item_image.save()
            new_item.images.add(item_image)
        return redirect('marketplace')
    return redirect('add_item')

    '''
    if request.FILES.get('item_pic'):
        item_pic = request.FILES['item_pic']
        clean_name = ''.join(c for c in identifier if c.isalnum() or c in '._- ')
        clean_name = clean_name.replace(' ', '_').lower()
        file_url = default_storage.save(f"media/item_pics/{clean_name}.png", item_pic)   
    '''

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_notifications(request):
    qs = Notification.objects.filter(user=request.user, read=False)
    serializer = NotificationSerializer(qs, many=True)
    return Response(serializer.data)

def collection(request):

    if request.method == "POST":
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.creator = request.user.profile  # Assign logged-in user as creator
            collection.save()
            form.save_m2m()  # Save ManyToMany relationships
            return redirect('collections')# Redirect to homepage after submission

    else:
        form = CollectionForm()

    collections = Collection.objects.all()
    user_collections = Collection.objects.filter(creator = request.user.profile)
    items = Item.objects.all()

    return render(request, 'collection.html', {'form': form, 'collections': collections, 'items' : items, 'user_collections': user_collections})

def collection_detail(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)
    items = collection.items.all()  # if you have a related_name like 'items' in FK
    return render(request, 'collection_detail.html', {
        'collection': collection,
        'items': items,
    })

def edit_collection(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)

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
    collection = get_object_or_404(Collection, pk=collection_id)
    CollectionAccessRequest.objects.get_or_create(user=request.user, collection=collection)
    return redirect('collection_detail', collection_id=collection.id)
@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})