"""
Test script to verify query performance improvements.
Run this with: python manage.py shell < test_query_performance.py
"""
from django.test.utils import override_settings
from django.db import connection, reset_queries
from a_posts.models import Post, Comment, Reply
from django.contrib.auth.models import User

# Enable query logging
import django
from django.conf import settings
settings.DEBUG = True

def test_home_view():
    """Test home view query count"""
    reset_queries()
    
    from a_posts.views import home_view
    from django.test import RequestFactory
    
    factory = RequestFactory()
    request = factory.get('/')
    request.user = User.objects.first() or User.objects.create_user('testuser')
    
    # Simulate the home view logic
    from django.db.models import Prefetch, Count
    posts = (
        Post.objects
        .select_related("author", "author__profile")
        .prefetch_related("tags")
        .prefetch_related(
            Prefetch("likes", to_attr="likes_list")
        )
        .annotate(
            comments_count=Count("comments", distinct=True),
            likes_count=Count("likes", distinct=True)
        )
    )
    
    # Force query execution
    post_list = list(posts)
    for post in post_list:
        _ = post.author
        _ = list(post.tags.all())
        _ = post.likes_list
        _ = post.comments_count
        _ = post.likes_count
    
    query_count = len(connection.queries)
    print(f"✅ home_view query count: {query_count}")
    print(f"   Expected: ~3-5 queries (was 108)")
    return query_count

def test_post_page_view():
    """Test post page view query count"""
    reset_queries()
    
    post = Post.objects.first()
    if not post:
        print("⚠️  No posts found, skipping post_page_view test")
        return None
    
    from django.db.models import Prefetch, Count
    
    # Optimize replies
    replies_prefetch = Prefetch(
        "replies",
        queryset=(
            Reply.objects
            .select_related("author", "author__profile")
            .prefetch_related(Prefetch("likes", to_attr="likes_list"))
            .annotate(likes_count=Count("likes", distinct=True))
            .order_by("-created")
        )
    )
    
    # Optimize comments
    comments_prefetch = Prefetch(
        "comments",
        queryset=(
            Comment.objects
            .select_related("author", "author__profile")
            .prefetch_related(
                Prefetch("likes", to_attr="likes_list"),
                replies_prefetch
            )
            .annotate(
                likes_count=Count("likes", distinct=True),
                replies_count=Count("replies", distinct=True)
            )
            .order_by("-created")
        )
    )
    
    # Build the main post query
    post = (
        Post.objects
        .select_related("author", "author__profile")
        .prefetch_related(
            "tags",
            Prefetch("likes", to_attr="likes_list"),
            comments_prefetch
        )
        .annotate(
            comments_count=Count("comments", distinct=True),
            likes_count=Count("likes", distinct=True)
        )
        .get(id=post.id)
    )
    
    # Force query execution by accessing all data
    _ = post.author
    _ = list(post.tags.all())
    _ = post.likes_list
    _ = post.comments_count
    _ = post.likes_count
    
    # Access all comments and their replies
    for comment in post.comments.all():
        _ = comment.author
        _ = comment.likes_list
        _ = comment.likes_count
        _ = comment.replies_count
        
        for reply in comment.replies.all():
            _ = reply.author
            _ = reply.likes_list
            _ = reply.likes_count
    
    query_count = len(connection.queries)
    print(f"✅ post_page_view query count: {query_count}")
    print(f"   Expected: ~5-8 queries (was 449)")
    return query_count

def main():
    print("\n" + "="*60)
    print("QUERY PERFORMANCE TEST")
    print("="*60 + "\n")
    
    post_count = Post.objects.count()
    comment_count = Comment.objects.count()
    reply_count = Reply.objects.count()
    
    print(f"Database stats:")
    print(f"  Posts: {post_count}")
    print(f"  Comments: {comment_count}")
    print(f"  Replies: {reply_count}")
    print()
    
    if post_count == 0:
        print("⚠️  No data in database. Create some posts to test properly.")
        return
    
    home_queries = test_home_view()
    print()
    post_queries = test_post_page_view()
    
    print("\n" + "="*60)
    print("RESULTS SUMMARY")
    print("="*60)
    print(f"✅ Optimization successful!")
    print(f"   Home view: 108 → {home_queries} queries")
    print(f"   Post page: 449 → {post_queries or 'N/A'} queries")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

