from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models

class Class(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    items = models.ManyToManyField('Item', related_name='classes', blank=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Item(models.Model):
    identifier = models.CharField(max_length=255, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, related_name='items', blank=True)

    def __str__(self):
        status = "Available" if self.is_available else "Not Available"
        tag_names = ", ".join(tag.name for tag in self.tags.all())
        return f"{tag_names} ({status})"


class TestObject(models.Model):
    important_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='media/profile_pics/', blank=True, null=True)
    userRole = models.IntegerField(default=0) #0 represents patron, 1 represents librarian
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

