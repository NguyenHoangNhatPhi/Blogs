from django.shortcuts import get_object_or_404

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
            
            return func(request, model_instance)
        return wrapper
    return inner_func