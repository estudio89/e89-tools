# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.http import HttpResponse

def any_permission_required(*args):
    """
    A decorator which checks user has any of the given permissions.
    permission required can not be used in its place as that takes only a
    single permission.
    """
    def test_func(user):
        for perm in args:
            if user.has_perm(perm):
                return True
        return False
    return user_passes_test(test_func)

def check_secret(func):
    ''' Checa em uma view, se foi passado um parâmetro 'secret' igual ao 'secret' em settings.py '''
    def wrapper(request):
        if request.method == "POST":
            if request.POST.get('secret','') != settings.SECRET_KEY:
                from django.core.exceptions import PermissionDenied
                raise PermissionDenied()
            return func(request)
        else:
            return HttpResponse('')
    return wrapper