from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm
from .models import Profile


def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(Profile, user__username=username)
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()
    return render(request, "a_users/profile.html", {"profile": profile})


@login_required
def edit_profile_view(request):
    form = ProfileForm(instance=request.user.profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    return render(request, "a_users/profile_edit.html", {"form": form})

@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, "Account deleted")
        return redirect("home")
    return render(request, "a_users/profile_delete.html")
