from django.contrib import admin


# Register your models here.
from .models import TestObject,Profile

admin.site.register(TestObject)
admin.site.register(Profile)

