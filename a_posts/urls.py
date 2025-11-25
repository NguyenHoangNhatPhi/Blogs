from django.urls import path
from .views import (
    home_view,
    post_create_view,
    post_delete_view,
    post_edit_view,
    post_page_view,
    comment_send,
    comment_delete,
    reply_send,
    reply_delete,
    like_post,
    like_comment,
)

urlpatterns = [
    path("", home_view, name="home"),
    path("category/<slug:slug>/", home_view, name="category"),
    path("post/create/", post_create_view, name="post-create"),
    path("post/delete/<uuid:post_id>/", post_delete_view, name="post-delete"),
    path("post/edit/<uuid:post_id>/", post_edit_view, name="post-edit"),
    path("post/<uuid:post_id>/", post_page_view, name="post"),
    path("post/<uuid:id>/like/", like_post, name="like-post"),
    path("commentsent/<uuid:comment_id>/", comment_send, name="comment-send"),
    path("comment/delete/<uuid:comment_id>/", comment_delete, name="comment-delete"),
    path("comment/<uuid:id>/like", like_comment, name="like-comment"),
    path("reply-send/<uuid:comment_id>/", reply_send, name="reply-send"),
    path("reply-delete/<uuid:reply_id>/", reply_delete, name="reply-delete"),
    
]
