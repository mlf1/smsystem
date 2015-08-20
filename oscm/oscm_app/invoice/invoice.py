# coding=utf-8
# oscm_app/invoice

# django imports
from django.db import models

# OSCM imports
from ..constants import INVOICES
from ..utils import get_attr


class Invoice(models.Model):

    """
    This class is used to represent the invoice.
    """

    class Meta:
        db_table = '%s_%s' % (get_attr('APP_NAME'), INVOICES)
