# coding=utf-8
# oscm_app/decorators

# django imports
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.utils.decorators import method_decorator


class UserCheckMixin(object):

    """
    check object can do permission
    only user is active
    if pass: go on
    if fail: redirect to fail path
    """
    # http://jsatt.com/blog/decorators-vs-mixins-for-django-class-based-views/
    user_check_failure_path = reverse_lazy('403')
    # reverse_lazy('oscm:home')

    def check_user(self, user):
        # check user is active
        return user is not None and user.is_active

    def user_check_failed(self, request, *args, **kwargs):
        # if check fail, redirect to fail path
        return redirect(self.user_check_failure_path)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # check permission
        if not self.check_user(request.user):
            return self.user_check_failed(request, *args, **kwargs)
        # if pass, go on
        return super(UserCheckMixin, self).dispatch(request, *args, **kwargs)
