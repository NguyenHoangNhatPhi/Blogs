from time import sleep
from django.db import models
import uuid


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    artist = models.CharField(max_length=500, null=True, blank=True)
    url = models.URLField(max_length=255, null=True)
    image = models.URLField(max_length=255)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created']

class Tag(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)
    order = models.IntegerField(null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']