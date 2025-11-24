from ast import Mod
from django.forms import ModelForm
from django import forms

from .models import Post, Comment, Reply


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ["url", "body", "tags"]
        labels = {"body": "Caption", "tags": "Categories"}
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Add a caption...",
                    "class": "font1 text-4xl",
                }
            ),
            "url": forms.TextInput(attrs={"placeholder": "Add url..."}),
            "tags": forms.CheckboxSelectMultiple(),
        }


class PostEditFrom(ModelForm):
    class Meta:
        model = Post
        fields = ["body", "tags"]
        labels = {"body": "", "tags": "Categories"}
        widgets = {
            "body": forms.Textarea(attrs={"rows": 3, "class": "font1 text-4xl"}),
            "tags": forms.CheckboxSelectMultiple(),
        }


class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        labels = {"body": ""}
        widgets = {
            "body": forms.TextInput(
                attrs={"placeholder": "Add a comment...", "class": "w-full"}
            ),
        }


class RepyCreateForm(ModelForm):
    class Meta:
        model = Reply
        fields = ["body"]
        labels = {
            "body": "",
        }
        widgets = {
            "body": forms.TextInput(
                attrs={
                    "placeholder": "Add reply...",
                    "class": "w-full !text-sm",
                }
            )
        }
