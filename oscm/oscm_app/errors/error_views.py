# coding=utf-8
# oscm_app/errors

from django.shortcuts import render
from django.http import HttpResponse
from django.template import (Context, loader, RequestContext)
from django.utils.translation import ugettext as _


def custom_proc(request):
    """
    A context processor that provides 'app', 'user' and 'ip_address'.
    """
    return {
        'app': 'oscm_app',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR']
    }


def error404(request, template_name='oscm_app/errors/404.html'):
    """
    Simple Handle 404 Errors
    """
    return render(request, template_name)


def error500(request, template_name='oscm_app/errors/500.html'):
    """
    Simple Handle 500 Errors
    """
    return render(request, template_name)


def page_not_found(request):
    """
    1. Load models for this view if necessary
    2. Generate Content for this view
    """
    template = loader.get_template('oscm_app/errors/404.html')
    context = {
        'message': 'All: %s' % request,
    }
    c = RequestContext(request, context)
    # 3. Return Template for this view + Data
    return HttpResponse(
        content=template.render(c),
        content_type='text/html; charset=utf-8',
        status=404)


def server_error(request):
    """
    1. Load models for this view
    2. Generate Content for this view
    """
    template = loader.get_template('oscm_app/errors/500.html')
    context = Context({
        'message': 'All: %s' % request,
        })
    # 3. Return Template for this view + Data
    return HttpResponse(
        content=template.render(context),
        content_type='text/html; charset=utf-8',
        status=500)


def permission_denied(request):
    """
    1. Load models for this view if necessary
    2. Generate Content for this view
    """
    template = loader.get_template('oscm_app/errors/403.html')
    context = {
        'message': 'All: %s' % request,
        'error_message': _("access to the view. ").format(request.path),
    }
    c = RequestContext(request, context, processors=[custom_proc])
    # 3. Return Template for this view + Data
    return HttpResponse(
        content=template.render(c),
        content_type='text/html; charset=utf-8',
        status=403)
