# coding=utf-8
# oscm_app/cart/catalogue/forms

# python imports
import logging

# django imports
from django import forms
from django.utils.translation import ugettext as _

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ObjectInterestForm(forms.ModelForm):

    """
    This class is the specific form of the OSCM object details.
    """
    has_been_modified = True

    error_messages = {
        'duplicate name': _('Duplicate name: %(name)s'),
        'invalid unit price': _('Invalid unit price: %(unit_price)s'),
        'invalid quantity': _('Invalid quantity: %(quantity)s'),
        'invalid date': _('Invalid date: %(date)s'),
        'wrong date': _(
            "Wrong date: requested due date(\'%(requested_due_date)s\') "
            "must be greater than the current date(\'%(today)s\')"),
    }

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop("initial", {})
        kwargs['initial'] = self.retrieve_initial_data(
            initial,
            **kwargs)
        super(ObjectInterestForm, self).__init__(*args, **kwargs)

    def retrieve_initial_data(self, initial, **kwargs):
        """
        Populate initial with its field values.
        """
        if kwargs.get("instance"):
            current_object = kwargs["instance"]
            for key in self.Meta.fields:
                print("KEY: %s" % key)
                if hasattr(current_object, key):
                    initial[key] = initial.get(key) or getattr(
                        current_object,
                        key)
        print("initial %s" % initial)
        return initial

    def check_update_value(self, model, key, value):
        if self.initial[key] == value:
            logger.debug(
                "No modificaton with the \'%s\' !! %s" % (key, value))
            return self.initial[key]
        else:
            logger.debug(
                "Return \'%s\' from the OSCM \'%s\': "
                "\'%s\'" % (key, model, value))
            return value

    def clean_description(self):
        return self.check_update_value(
            'object details',
            'description',
            self.cleaned_data['description'])

    def clean_is_active(self):
        return self.check_update_value(
            'object details',
            'is_active',
            self.cleaned_data['is_active'])

    def clean(self):
        pass

    def save(self, commit=True):
        pass
