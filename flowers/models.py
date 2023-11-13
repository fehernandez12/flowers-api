from django.db import models

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    checksum = models.CharField(max_length=255, blank=True, null=True)
    prediction = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)