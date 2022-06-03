from django.db import models

# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(max_length=10, null=True, blank=True)
    tags = models.CharField(max_length=100, null=True, blank=True)
    document = models.CharField(max_length=1000, null=True, blank=True)