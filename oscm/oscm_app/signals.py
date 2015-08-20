# coding=utf-8
# oscm_app

# django imports
from django.dispatch import Signal

# Product
product_changed = Signal()

# Category
category_deleted = Signal(providing_args=['request'])
category_updated = Signal(providing_args=["category", "form"])
category_changed = Signal()

# Cart
cart_changed = Signal()

# Cart item
cart_item_changed = Signal()

# Order
order_changed = Signal()

# Order item
order_item_changed = Signal()
