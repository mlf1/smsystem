# coding=utf-8
# oscm_app/cart/catalogue/forms

# python imports
import logging

# django imports
from django import forms
from django.utils.translation import ugettext as _

# OSCM imports
from ....utils import set_form_field_order
from ..models.category import Category

# Get an instance of a logger
logger = logging.getLogger(__name__)


class CategoryForm(forms.ModelForm):

    """
    This class is the specific form of the OSCM Category.
    """

    class Meta:

        """
        Use this Meta class on any model to specify various
        model-specific options.
        """
        model = Category
        fields = (
            'name',
            'description',
            'is_active',
        )

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        set_form_field_order(self, ["name", "description", "is_active"])

    def save(self, commit=True):
        """
        Save the provided password in hashed format
        """
        category = super(forms.ModelForm, self).save(
            commit=False)
        return self.save_category(category, commit)

    def save_category(self, category, commit=True):
        """
        Save the category of the OSCM User if it is necessary.
        """
        if commit:
            category.save()
            logger.info(
                _(
                    "OSCM Category \'%s\' has "
                    "been created." % category.name))
            return category
