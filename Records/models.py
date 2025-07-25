from django.db import models
from django.conf import settings

class Record(models.Model):
    TEMPLATE_CHOICES = (('content', 'Content'),)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='records')
    template = models.CharField(max_length=50, choices=TEMPLATE_CHOICES, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    api_thumbnail = models.URLField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    content_title = models.CharField(max_length=255, null=True, blank=True)
    creator = models.JSONField(null=True, blank=True)
    cast = models.JSONField(null=True, blank=True)
    story = models.TextField(null=True, blank=True)
    scenes = models.TextField(null=True, blank=True)
    thoughts = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    companions = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class RecordImage(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='image_urls')
    image = models.ImageField(upload_to='record_images/', null=True, blank=True)

class Element(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='elements')
    shape = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    angle_x = models.IntegerField(null=True, blank=True)
    angle_y = models.IntegerField(null=True, blank=True)
    angle_z = models.IntegerField(null=True, blank=True)
    position_x = models.IntegerField(null=True, blank=True)
    position_y = models.IntegerField(null=True, blank=True)
    position_z = models.IntegerField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
