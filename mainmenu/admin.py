from django.contrib import admin


# Register your models here.
from .models import TestObject

admin.site.register(TestObject)

