from django.contrib import admin

from .models import *

models = [Post, Tag, Comment, Reply, LikedPost, LikedComment, LikedReply]
for model in models:
    admin.site.register(model)
