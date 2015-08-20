# coding=utf-8
# oscm_app

# django imports
from django.apps import AppConfig

# OSCM imports
from .utils import get_attr


class OSCMConfig(AppConfig):

    name = get_attr('APP_NAME')
    verbose_name = get_attr('VERBOSE_APP_NAME')

    def ready(self):
        """
        Import signals.handlers
        """
        import oscm_app.handlers
