from django.shortcuts import render, redirect, get_object_or_404
from bs4 import BeautifulSoup
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Post, Tag
from .forms import PostCreateForm, PostEditFrom, CommentCreateForm


def home_view(request, slug=None):
    # Optimize query to prefetch related tags to avoid N+1 queries
    tag = None
    if slug:
        posts = Post.objects.prefetch_related("tags").filter(tags__slug=slug)
        tag = get_object_or_404(Tag, slug=slug)
    else:
        posts = Post.objects.prefetch_related("tags").all()
    categories = Tag.objects.all()
    context = {"posts": posts, "categories": categories, "tag": tag}
    return render(request, "a_posts/home.html", context)

@login_required
def post_create_view(request):
    form = PostCreateForm()
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            website = requests.get(form.data["url"])
            sourcecode = BeautifulSoup(website.text, "html.parser")

            find_image = sourcecode.select(
                'meta[content^="https://live.staticflickr.com/"]'
            )
            try:
                image = find_image[0]["content"]
            except:
                messages.error(request, "Requested image is not on Flickr!")
                return redirect("post-create")

            post.image = image

            find_title = sourcecode.select("h1.photo-title")
            title = find_title[0].text.strip()
            post.title = title

            find_artist = sourcecode.select("a.owner-name")
            artist = find_artist[0].text.strip()
            post.artist = artist

            post.author = request.user

            post.save()
            form.save_m2m()
            return redirect("home")
        else:
            return render(request, "a_posts/post_create.html", {"form": form})
    return render(request, "a_posts/post_create.html", {"form": form})


@login_required
def post_delete_view(request, id):
    # Optimize query to prefetch related tags
    post = get_object_or_404(
        Post.objects.prefetch_related("tags"), id=id, author=request.user
    )

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted")
        return redirect("home")

    return render(request, "a_posts/post_delete.html", {"post": post})

@login_required
def post_edit_view(request, id):
    # Optimize query to prefetch related tags
    post = get_object_or_404(
        Post.objects.prefetch_related("tags"), id=id, author=request.user
    )
    form = PostEditFrom(instance=post)
    if request.method == "POST":
        form = PostEditFrom(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated")
            return redirect("home")
    context = {"post": post, "form": form}

    return render(request, "a_posts/post_edit.html", context)


def post_page_view(request, id):
    # Optimize query to prefetch related tags
    post = get_object_or_404(Post.objects.prefetch_related("tags"), id=id)
    commentform = CommentCreateForm()
    context = {"post": post, "commentform": commentform}
    
    return render(request, "a_posts/post_page.html", context)

