from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    required_tags = models.ManyToManyField(Tag, related_name='required_by', blank=True)

    def __str__(self):
        return self.name


class ItemImage(models.Model):
    image = models.ImageField(upload_to='item_images/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.caption or f"Image {self.id}"


class Item(models.Model):
    STATUS_AVAILABLE = 'available'
    STATUS_IN_CIRCULATION = 'in_circulation'
    STATUS_REPAIRING = 'repairing'
    STATUS_LOST = 'lost'
    STATUS_CHOICES = [
        (STATUS_AVAILABLE, 'Available'),
        (STATUS_IN_CIRCULATION, 'In Circulation'),
        (STATUS_REPAIRING, 'Being Repaired'),
        (STATUS_LOST, 'Lost'),
    ]
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE)
    location = models.CharField(max_length=255, blank=True, help_text="e.g. home library, work library")
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, related_name='items', blank=True)
    images = models.ManyToManyField(ItemImage, related_name='items', blank=True)
    collections = models.ManyToManyField('Collection', related_name='items_of', blank=True)

    def __str__(self):
        status_display = dict(self.STATUS_CHOICES).get(self.status, self.status)
        tag_list = ", ".join(tag.name for tag in self.tags.all())
        return f"{self.title} [{status_display}] – Tags: {tag_list or 'None'}"


class TestObject(models.Model):
    important_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='media/profile_pics/', blank=True, null=True)
    userRole = models.IntegerField(default=0) #0 represents patron, 1 represents librarian
    def __str__(self):
        return self.user.username

class Collection(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    VISIBILITY_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank = True)
    items = models.ManyToManyField(Item, related_name='collections_of')
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name = "collections")
    visibility = models.CharField(
        max_length=8,
        choices=VISIBILITY_CHOICES,
        default=PUBLIC
    )
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Ensure only librarians can create private collections."""
        if self.creator.userRole == 0:  # If creator is a patron
            self.visibility = self.PUBLIC  # Force visibility to Public
        super().save(*args, **kwargs)
        # If the collection is private, check the items
        if self.visibility == self.PRIVATE:
            # Check if any of the items in this collection are already in another private collection
            for item in self.items.all():
                # Query to find other collections with the same item and private visibility
                if Collections.objects.filter(items=item, visibility=self.PRIVATE).exclude(id=self.id).exists():
                    raise ValidationError(f"Item '{item.identifier}' is already in another private collection.")

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

