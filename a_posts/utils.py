from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, Count

def like_toggle(model):
    def inner_func(func):
        def wrapper(request, *args, **kwargs):
            model_instance = get_object_or_404(model, id=kwargs.get("id"))
            user_exist = model_instance.likes.filter(username=request.user.username).exists()
            
            if model_instance.author != request.user:
                if user_exist:
                    model_instance.likes.remove(request.user)
                else:
                    model_instance.likes.add(request.user)
            
            # Reload the object with optimizations for template rendering
            model_instance = (
                model.objects
                .select_related("author", "author__profile")
                .prefetch_related(Prefetch("likes", to_attr="likes_list"))
                .annotate(likes_count=Count("likes", distinct=True))
                .get(id=model_instance.id)
            )
            
            return func(request, model_instance)
        return wrapper
    return inner_func