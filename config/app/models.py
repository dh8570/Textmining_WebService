from django.db import models

# Create your models here.
class Document(models.Model):
    text = models.CharField(max_length=1000)
    label = models.CharField(max_length=10)
    tags = models.CharField(max_length=100)