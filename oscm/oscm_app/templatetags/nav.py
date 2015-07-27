# coding=utf-8
# oscm_app/templatetags

# python imports
import re

# django imports
from django import template

# OSCM imports
from ..cart.catalogue.category import Category

register = template.Library()


@register.simple_tag
def active(request, pattern, exact_match=False):
    if exact_match:
        if not pattern.startswith('^'):
            pattern = '^' + pattern
        if not pattern.endswith('$'):
            pattern += '$'
    if hasattr(request, 'path') and re.search(pattern, request.path):
        return 'active'
    return ''


@register.inclusion_tag('oscm_app/cart/catalogue/cats.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all(), 'act_cat': cat}
