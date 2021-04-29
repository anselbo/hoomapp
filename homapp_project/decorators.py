from django.shortcuts import redirect
from django.contrib import messages

def only_admin(view):
    def wrapper_view(request, *args, **kwargs):
        if request.user.is_staff == True and request.user.is_superuser == True:
            return view(request, *args, **kwargs)
        else:
            messages.error(request, f'{request.user.username}, you are not authorized to that page')
            return redirect('logout')
    return wrapper_view



def unauthorized_user(view):
    def wrapper_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view(request, *args, **kwargs)
    return wrapper_view