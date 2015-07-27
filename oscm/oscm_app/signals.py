# coding=utf-8

# django imports
import django.dispatch

# Product
product_changed = django.dispatch.Signal()

# Category
category_changed = django.dispatch.Signal()

# Cart
cart_changed = django.dispatch.Signal()

# Cart item
cart_item_changed = django.dispatch.Signal()

# Order
order_changed = django.dispatch.Signal()

# Order item
order_item_changed = django.dispatch.Signal()
