from django.shortcuts import render, redirect, get_object_or_404


from .forms import ProfileForm
from .models import Profile

def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(Profile, user__username=username)
    profile = request.user.profile
    return render(request,"a_users/profile.html", {"profile": profile})

def edit_profile_view(request):
    form = ProfileForm(instance=request.user.profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES ,instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, 'a_users/profile_edit.html', {"form": form})