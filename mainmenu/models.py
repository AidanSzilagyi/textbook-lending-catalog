from django.db import models

# Create your models here.
class TestObject(models.Model):
    important_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

class Account(models.Model):
    user = models.CharField("user", max_length=200)
    email = models.CharField("email", max_length=200)
    password = models.CharField("password", max_length=200)
    