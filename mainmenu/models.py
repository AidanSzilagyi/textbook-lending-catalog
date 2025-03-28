from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Class(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Item(models.Model):
    tags = models.ManyToManyField(Tag, related_name='items')
    identifier = models.CharField(max_length=255, blank=True, null=True)
    is_available = models.BooleanField(default=True)

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

class Collections(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    VISIBILITY_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank = True)
    items = models.ManyToManyField(Item, related_name='collections')
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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

