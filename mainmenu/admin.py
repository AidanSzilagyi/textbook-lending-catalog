from django.contrib import admin
from django_celery_beat.models import PeriodicTask, IntervalSchedule

# Register your models here.
from .models import TestObject,Profile, Class, Tag, Item, Collection

from mainmenu.models import Tag

admin.site.register(TestObject)
admin.site.register(Class)
admin.site.register(Item)
admin.site.register(Collection)
class ProfileAdmin(admin.ModelAdmin):
    # Define which fields to display in the admin list view
    list_display = ('user', 'user_username', 'user_email', 'userRole', 'user_first_name', 'user_last_name', 'user_password')

    # Custom method to display the username of the associated User model
    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Username'  # Optional: Set a custom header for this column

    # Custom method to display the email of the associated User model
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'

    # You can add more custom methods to show other User fields if needed
    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = 'First Name'

    def user_last_name(self, obj):
        return obj.user.last_name
    user_last_name.short_description = 'Last Name'

    def user_password(self, obj):
        return obj.user.password
    user_password.short_description = 'Password'

admin.site.register(Profile, ProfileAdmin)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass