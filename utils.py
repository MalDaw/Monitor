import functools


def add_metadata(title=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            return {
                "title": title or func.__name__,
                "data": data
            }
        return wrapper
    return decorator