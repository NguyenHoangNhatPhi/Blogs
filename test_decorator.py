def inner_func(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def tinh_tong(a,b):
    return a + b

wrapper = inner_func(tinh_tong) 
wrapper(1,2)