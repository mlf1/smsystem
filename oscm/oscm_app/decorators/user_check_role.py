# coding=utf-8
# oscm_app/decorators

# python imports
from functools import wraps

# django imports
from django.core.exceptions import PermissionDenied


class UserCheckRole(object):

    """
    check object can do permission
    only user is active
    if pass: go on
    if fail: redirect to fail path
    """

    def has_role_decorator(self, role):
        def request_decorator(dispatch):
            @wraps(dispatch)
            def wrapper(request, *args, **kwargs):
                user = request.user
                if user.is_authenticated():
                    if role == 'M':
                        return dispatch(request, *args, **kwargs)
                    """
                    if has_role(user, role):
                        return dispatch(request, *args, **kwargs)
                    """
                raise PermissionDenied
            return wrapper
        return request_decorator
