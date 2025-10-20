from django.urls import path
from .views import home_view, post_create_view, post_delete_view, post_edit_view, post_page_view

urlpatterns = [
    path("", home_view, name="home"),
    path("post/create/", post_create_view, name="post-create"),
    path("post/delete/<uuid:id>/", post_delete_view, name="post-delete"),
    path("post/edit/<uuid:id>/", post_edit_view, name="post-edit"),
    path("post/<uuid:id>/", post_page_view, name="post")
]
