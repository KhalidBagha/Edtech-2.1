from tokenize import group
from urllib import request
from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_url):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated:
            g = request.user.group.all()[0].name
            if g == "admin":
                 return redirect('dash')
            else:
                 return redirect('studentpanel')

        else:
             return view_url(request,*args, **kwargs)
    return wrapper_func

def admin_only(view_func):
    def wrapper_functon(request,*args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                
                if group == "student":
                    return redirect('studentpanel')
                if group == "admin":
                    return view_func(request,*args, **kwargs)

    return wrapper_functon