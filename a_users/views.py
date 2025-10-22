from django.shortcuts import render

from .models import Profile

def profile_view(request):
    profile = request.user.profile
    return render(request,"a_users/profile.html", {"profile": profile})

def edit_profile_view(request):
    return render(request, 'a_users/profile_edit.html')