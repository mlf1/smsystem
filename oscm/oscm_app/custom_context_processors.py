# coding=utf-8
# oscm_app

from .utils import get_attr


def retrieve_setting_parameters(request):
    """
    Retrieve some parameters from the settings file
    """
    # REGISTRATION_OPEN
    reg_allowed = get_attr('REGISTRATION_OPEN', False)
    # REGISTRATION_AUTO_ACTIVATED_ACCOUNT
    reg_auto_activated_account = get_attr(
        'REGISTRATION_AUTO_ACTIVATED_ACCOUNT', False)
    return {
        'request': request,
        'registration_allowed': reg_allowed,
        'registration_auto_activated_account': reg_auto_activated_account
    }
