def override(**kwargs):
    def wrapped_function(func):
        for key, value in kwargs.items():
            setattr(func, key, value)
        return func

    return wrapped_function
