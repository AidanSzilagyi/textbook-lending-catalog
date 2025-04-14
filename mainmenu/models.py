from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
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


class Collection(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

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
    STATUS_REQUESTED = 'requested'
    STATUS_CHOICES = [
        (STATUS_AVAILABLE, 'Available'),
        (STATUS_IN_CIRCULATION, 'In Circulation'),
        (STATUS_REPAIRING, 'Being Repaired'),
        (STATUS_LOST, 'Lost'),
        (STATUS_REQUESTED, 'Requested'),
    ]
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE)
    location = models.CharField(max_length=255, blank=True, help_text="e.g. home library, work library")
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, related_name='items', blank=True)
    images = models.ManyToManyField(ItemImage, related_name='items', blank=True)
    collections = models.ManyToManyField(Collection, related_name='items', blank=True)
    due_date = models.DateField(
        blank=True,
        null=True,
        help_text="When this item is due back."
    )
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='borrowed_items',
        blank=True,
        null=True,
        help_text="The user who currently has this item checked out."
    )

    @property
    def is_overdue(self):
        if not self.due_date:
            return False
        return timezone.localdate() > self.due_date

    def days_until_due(self):
        if not self.due_date:
            return None
        delta = self.due_date - timezone.localdate()
        return delta.days

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

class Notification(models.Model):
    KINDS = [
      ('one_week','One Week Out'),
      ('one_day','One Day Out'),
      ('one_hour','One Hour Out'),
    ]
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    item      = models.ForeignKey(Item, on_delete=models.CASCADE)
    kind      = models.CharField(max_length=20, choices=KINDS)
    created   = models.DateTimeField(auto_now_add=True)
    read      = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user','item','kind')

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} to {self.recipient}: {self.content[:30]}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

