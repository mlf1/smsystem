# coding=utf-8
# oscm_app/cart/catalogue

# django imports
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

# OSCM imports
from ...constants import CATEGORIES
from ...utils import get_attr
from ..cart_manager import CartQuerySet
from .product import Product


class Category(models.Model):

    """
    This class is used to represent the Category for the products.
    It's used to browse through the catalog products.
    """

    # Category name
    name = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        unique=True)
    # Slug name : part of the URL
    slug_name = models.SlugField(max_length=120, unique=True, blank=False)
    # Short description about the category
    description = models.TextField(
        verbose_name=_('oscm_admin_descriptionOfCategory'),
        blank=True,
        help_text=_('oscm_admin_helpTextDescriptionOfCategory'),
    )
    # Creation date
    creation_date = models.DateTimeField(
        verbose_name=_('oscm_admin_creationDateOfCategory'), auto_now_add=True)
    # Last edit date
    last_edit_date = models.DateTimeField(
        verbose_name=_('oscm_admin_lastEditDateOfCategory'), auto_now=True)
    # Active status, if False the category won't be displayed to shop users.
    is_active = models.BooleanField(
        verbose_name=_('oscm_admin_displayOfCategory'),
        help_text=_('oscm_admin_helpTextActiveStatusOfCategory'),
        default=False,
        null=False,
    )

    class Meta:
        ordering = ["name", ]
        verbose_name = _('oscm_admin_headerOfCategory')
        verbose_name_plural = _('oscm_admin_headerOfCategories')
        db_table = '%s_%s' % (get_attr('APP_NAME'), CATEGORIES)

    objects = CartQuerySet.as_manager()

    def __str__(self):
        """
        Displays the name of categories.
        """
        return _("category (name: %s)") % self.name

    def get_active_products(self):
        """
        Retrieves all active products for a given category.
        """
        return Product.objects.filter(category=self).filter(is_active=True)

    def get_products(self):
        """
        Retrieves all products for a given category.
        """
        return Product.objects.filter(category=self)

    def get_absolute_url(self):
        # reverse('oscm:category', args=[self.slug_name])
        print("CAT: %s" % self.name)
        return reverse(
            'oscm:category',
            kwargs={'slug_name': self.slug_name})
