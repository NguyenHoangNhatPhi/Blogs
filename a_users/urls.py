from django.urls import path

from .views import profile_view, edit_profile_view, profile_delete_view

urlpatterns = [
    path("", profile_view, name="profile"),
    path("edit/", edit_profile_view, name="profile-edit"),
    path("delete/", profile_delete_view, name="profile-delete"),
    path("<str:username>/", profile_view, name="user-profile"),
]
