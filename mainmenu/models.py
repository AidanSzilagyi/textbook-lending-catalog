from django.db import models

# Create your models here.
class TestObject(models.Model):
    important_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")