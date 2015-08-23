# coding=utf-8
# oscm_app/cart/models

# django imports
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

# OSCM imports
from ...constants import CARTS, CART_STATUSES, DEFAULT_CART_STATUS
from ...utils import get_attr
from ..cart_manager import CartQuerySet
from .cart_item import CartItem


class Cart(models.Model):

    """
    This class is used to represent the Cart for the users.
    """

    # Owner of the cart
    owner = models.ForeignKey(
        get_attr('AUTH_USER_MODEL'),
        blank=False,
        related_name='carts',
        verbose_name=_("oscm_admin_ownerOfCart"),
        help_text=_('oscm_admin_helpTextOwnerOfCart'),
        limit_choices_to={'role': get_attr('DEFAULT_ROLE')},
    )

    # Project name
    project_name = models.CharField(
        verbose_name=_('oscm_admin_projectNameOfCart'),
        help_text=_('oscm_admin_helpTextProjectNameOfCart'),
        max_length=250,
        blank=False,
        null=False
    )

    # Creation date
    creation_date = models.DateTimeField(
        verbose_name=_('oscm_admin_creationDateOfCart'),
        auto_now_add=True,
    )
    # Last edit date
    last_edit_date = models.DateTimeField(
        verbose_name=_('oscm_admin_lastEditDateOfCart'),
        auto_now=True,
    )
    # Requested due date
    requested_due_date = models.DateTimeField(
        verbose_name=_('oscm_admin_requestedDueDateOfCart'),
        help_text=_('oscm_admin_helpTextRequestedDueDateOfCart'),
    )

    # Default parameter for the status attribute
    DEFAULT_CART_STATUS = get_attr(DEFAULT_CART_STATUS)
    # Retrieved the different statuses from the settings file
    CART_STATUSES = get_attr(CART_STATUSES)
    # Status
    status = models.IntegerField(
        verbose_name=_('oscm_admin_statusOfCart'),
        max_length=32,
        default=DEFAULT_CART_STATUS,
        choices=CART_STATUSES,
        help_text=_('oscm_admin_helpTextStatusOfCart'),
    )
    # Short description about the cart
    description = models.TextField(
        verbose_name=_("oscm_admin_descriptionOfCart"),
        blank=True,
        help_text=_('oscm_admin_helpTextDescriptionOfCart'),
    )
    # Item count (not equal to quantity, but distinct item count)

    class Meta:
        ordering = ["status", "creation_date", ]
        db_table = '%s_%s' % (get_attr('APP_NAME'), CARTS)
        verbose_name = _('oscm_admin_headerOfCart')
        verbose_name_plural = _('oscm_admin_headerOfCarts')

    objects = CartQuerySet.as_manager()

    def __str__(self):
        """
        Displays the status, the owner, the project
        name and the number of cart items.
        """
        return _(
            "cart (status: %(status)s, owner: %(owner)s, project name: "
            "%(project_name)s, number of cart items: %(nb_cart_items)d)"
        ) % {
            'status': self.CART_STATUSES[self.status][1],
            'owner': self.owner,
            'project_name': self.project_name,
            'nb_cart_items': self.nb_cart_items
        }

    def get_cart_items(self):
        """
        Retrieves all cart items for a given cart.
        """
        return CartItem.objects.filter(cart=self)

    @property
    def nb_cart_items(self):
        """
        Retrieves the number of distinct cart items for a given cart.
        """
        return CartItem.objects.filter(cart=self).count()

    @property
    def is_empty(self):
        """
        Test if this cart is empty.
        """
        return self.id is None or self.nb_cart_items == 0

    def get_absolute_url(self):
        return reverse(
            'oscm:cart',
            kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse(
            'oscm:delete_cart',
            kwargs={'pk': self.pk})
