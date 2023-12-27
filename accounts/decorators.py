from django.shortcuts import redirect


def unauthenticadeUser(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if 'admin' in request.user.groups.all():
                return redirect('home')
            else:
                return request('user')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            groups = None

            if request.user.groups.exists():
                groups = request.user.groups.all()

            for group in groups:
                if group.name in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    return redirect('user')

        return wrapper_func
    return decorator
