# coding=utf-8
# oscm_app/cart

# django imports
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

# OSCM imports
from ..constants import CARTS, CART_STATUSES, DEFAULT_CART_STATUS
from ..utils import get_attr


class Cart(models.Model):

    """
    This class is used to represent the Cart for the users.
    """

    # Owner of the cart
    owner = models.ForeignKey(
        get_user_model(),
        related_name='carts',
        verbose_name=_("oscm_admin_ownerOfCart"),
        limit_choices_to={'role': get_attr('DEFAULT_ROLE')},
    )

    # Project name
    project_name = models.CharField(
        verbose_name=_('oscm_admin_projectNameOfCart'),
        help_text=_('oscm_admin_helpTextProjectNameOfCart'),
        max_length=250,
        blank=True,
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
    status = models.CharField(
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
        db_table = "%(app_label)s_" + CARTS
        verbose_name = _('oscm_admin_headerOfCart')
        verbose_name_plural = _('oscm_admin_headerOfCarts')

    def __str__(self):
        """
        Displays the status, the owner and the number of carts.
        """
        return _(
            "%(status)s cart (owner: %(owner)s, project_name: "
            "%(project_name)s, lines: %(num_lines)d)") \
            % {
                'status': self.status,
                'owner': self.owner,
                'project_name': self.project_name,
                'num_lines': self.num_lines}

    @property
    def is_empty(self):
        """
        Test if this cart is empty.
        """
        return self.id is None or self.num_lines == 0
