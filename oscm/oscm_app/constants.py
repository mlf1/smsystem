# coding=utf-8
# oscm_app

"""
Specific constants to the OSCM application.
"""

# Default parameter for 'first_name' value.
ADMIN_FIRST_NAME = '<FIRSTNAME>'
# Default parameter for 'last_name' value.
ADMIN_LAST_NAME = '<LASTNAME>'

# Suppliers
SUPPLIERS = 'suppliers'

# Categories
CATEGORIES = 'categories'

# Products
PRODUCTS = 'products'

# Carts
CARTS = 'carts'

# Cart items
CART_ITEMS = 'cart_items'

# Orders
ORDERS = 'orders'

# Order items
ORDER_ITEMS = 'order_items'

# Invoices
INVOICES = 'invoices'

# Default cart status
DEFAULT_CART_STATUS = 'CART_STATUS_CREATED'

# Cart statuses
CART_STATUSES = 'CART_STATUSES'

# Default cart item status
DEFAULT_CART_ITEM_STATUS = 'CART_ITEM_STATUS_CREATED'

# Cart item statuses
CART_ITEM_STATUSES = 'CART_ITEM_STATUSES'

# Default order status
DEFAULT_ORDER_STATUS = 'ORDER_STATUS_CREATED'

# Order statuses
ORDER_STATUSES = 'ORDER_STATUSES'

# Default order item status
DEFAULT_ORDER_ITEM_STATUS = 'ORDER_ITEM_STATUS_CREATED'

# Order item statuses
ORDER_ITEM_STATUSES = 'ORDER_ITEM_STATUSES'

# Order base (this parameter can be set in settings for the next if necessary)
ORDER_BASE = 100000

# Default roles
ADMIN_ROLE = 'A'
MANAGER_ROLE = 'M'
USER_ROLE = 'U'

# Signals
CATEGORY_DELETED_SIGNAL = 'category_deleted_signal'
CATEGORY_UPDATED_SIGNAL = 'category_updated_signal'
PRODUCT_DELETED_SIGNAL = 'product_deleted_signal'
SUPPLIER_DELETED_SIGNAL = 'supplier_deleted_signal'
