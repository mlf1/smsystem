# coding=utf-8
# oscm_app/order

# django imports
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

# OSCM imports
from ..constants import DEFAULT_ORDER_STATUS, ORDER_STATUSES, ORDERS
from ..utils import OrderNumberGenerator, get_attr


class Order(models.Model):

    """
    The main order model.
    An order can be just created or modified by an OSCM Manager.
    Attributes:
        managed_by:
            OSCM Manager
        notes:
            error, information...
        cart_id:
            Cart (from Cart, order deleted --> cart deleted)
        date:
            creation_date (entry in DB)
            last_edit_date
            delivery_date
            due_date (max requested_due_date from Cart and delivery_date)
        status:
            deleted (not visible by OSCM User)
            submitted
            cancelled (appears always in the DB)
            validated
            checked
            completed
            archived (not visible for OSCM User)
        order_id:
            generator of order_id
        invoice_id:
            Invoice (from Invoice, order deleted --> invoice deleted)
    """

    # Default parameter for the status attribute
    DEFAULT_ORDER_STATUS = get_attr(DEFAULT_ORDER_STATUS)
    # Retrieved the different statuses from the settings file
    ORDER_STATUSES = get_attr(ORDER_STATUSES)
    # User of the Order
    managed_by = models.ForeignKey(
        get_user_model(),
        related_name='orders',
        null=True,
        limit_choices_to={'role': 'M'},
    )
    # Cart
    cart = models.ForeignKey('cart')
    # Invoice
    invoice = models.ForeignKey('invoice', null=True)
    # Generate order number
    ord_num_gen = OrderNumberGenerator()
    # Order id
    order_id = models.CharField(
        verbose_name=_('oscm_admin_orderIdOfOrder'),
        max_length=100,
        editable=False,
        unique=True,
        default=ord_num_gen.generate_order_number(cart=cart),
    )
    # Status
    status = models.CharField(
        verbose_name=_('oscm_admin_statusOfOrder'),
        max_length=32,
        default=DEFAULT_ORDER_STATUS,
        choices=ORDER_STATUSES,
        help_text=_('oscm_admin_helpTextStatusOfOrder'),
    )
    # Creation date
    creation_date = models.DateTimeField(
        verbose_name=_('oscm_admin_creationDateOfOrder'), auto_now_add=True)
    # Last edit date
    last_edit_date = models.DateTimeField(
        verbose_name=_('oscm_admin_lastEditDateOfOrder'), auto_now=True)
    # Due date
    due_date = models.DateTimeField(
        verbose_name=_('oscm_admin_dueDateOfOrder'),
        help_text=_('oscm_admin_helpTextDueDateOfOrder'),
    )
    # Delivery date
    delivery_date = models.DateTimeField(
        verbose_name=_('oscm_admin_deliveryDateOfOrder'),
        help_text=_('oscm_admin_helpTextDeliveryDateOfOrder'),
    )
    # Notes
    notes = models.TextField(
        verbose_name=_('oscm_admin_notesOfOrder'),
        blank=True,
        help_text=_('oscm_admin_helpTextNotesOfOrder'),
    )
    # Total
    total = models.DecimalField(
        _('oscm_admin_totalOfOrder'),
        decimal_places=2,
        max_digits=12)

    class Meta:
        db_table = '%s_%s' % (get_attr('APP_NAME'), ORDERS)
        ordering = ["creation_date", "status", ]
        verbose_name = _('oscm_admin_headerOfOrder')
        verbose_name_plural = _("oscm_admin_headerOfOrders")

    def __str__(self):
        """
        Displays the status, the project name and the order id of orders.
        """
        return _(
            "%(status)s order (order_id: %(order_id)d)") \
            % {
                'status': self.status,
                'order_id': self.order_id}
