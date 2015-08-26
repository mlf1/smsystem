# coding=utf-8
# oscm_app/templatetags

# python imports
import re

# django imports
from django import template

# OSCM imports
from ..cart.catalogue.models.category import Category
from ..cart.catalogue.models.product import Product
from ..cart.catalogue.models.supplier import Supplier
from ..cart.models.cart import Cart
from ..constants import (
    ADMIN_ROLE,
    DEFAULT_CART_STATUS,
    MANAGER_ROLE,
    USER_ROLE
)
from ..utils import get_attr

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
def get_category_list(request, is_menu=False, cat=None, role=USER_ROLE):
    if role == ADMIN_ROLE:
        return {
            'cats': Category.objects.all(),
            'act_cat': cat,
            'is_menu': is_menu,
            'request': request}
    elif role == MANAGER_ROLE or role == USER_ROLE:
        return {
            'cats': Category.objects.active().all(),
            'act_cat': cat,
            'is_menu': is_menu,
            'request': request}
    else:
        return {
            'cats': Category.objects.active().all(),
            'act_cat': cat,
            'is_menu': is_menu,
            'request': request}


@register.inclusion_tag('oscm_app/cart/catalogue/sups.html')
def get_supplier_list(request, is_menu=False, sup=None, role=USER_ROLE):
    if role == ADMIN_ROLE:
        return {
            'sups': Supplier.objects.all(),
            'act_sup': sup,
            'is_menu': is_menu,
            'request': request}
    elif role == MANAGER_ROLE or role == USER_ROLE:
        return {
            'sups': Supplier.objects.active().all(),
            'act_sup': sup,
            'is_menu': is_menu,
            'request': request}
    else:
        return {
            'sups': Supplier.objects.active().all(),
            'act_sup': sup,
            'is_menu': is_menu,
            'request': request}


@register.inclusion_tag('oscm_app/cart/catalogue/prods.html')
def get_product_list(
        request, is_menu=False, prod=None, role=USER_ROLE, inheritance=False):
    if role == ADMIN_ROLE:
        return {
            'prods': Product.objects.all(),
            'act_prod': prod,
            'is_menu': is_menu,
            'request': request}
    elif role == MANAGER_ROLE or role == USER_ROLE:
        if inheritance:
            return {
                'prods': Product.objects.active().filter(
                    category__is_active=True),
                'act_prod': prod,
                'is_menu': is_menu,
                'request': request}
        else:
            return {
                'prods': Product.objects.active().all(),
                'act_prod': prod,
                'is_menu': is_menu,
                'request': request}
    else:
        return {
            'prods': Product.objects.active().all(),
            'act_prod': prod,
            'is_menu': is_menu,
            'request': request}


@register.inclusion_tag('oscm_app/cart/cts.html')
def get_carts_list(request, cart=None, user=None):
    if user.role == ADMIN_ROLE:
        return {
            'cts': Cart.objects.all(),
            'act_cart': cart,
            'request': request,
            'user_id': user.id}
    elif user.role == MANAGER_ROLE:
        return {
            'cts': Cart.objects.exclude(status=get_attr(DEFAULT_CART_STATUS)),
            'act_cart': cart,
            'request': request,
            'user_id': user.id}
    elif user.role == USER_ROLE:
        return {
            'cts': Cart.objects.filter(owner=user),
            'act_cart': cart,
            'request': request,
            'user_id': user.id}
    else:
        return {
            'cts': Cart.objects.all(),
            'act_cart': cart,
            'request': request,
            'user_id': user.id}
