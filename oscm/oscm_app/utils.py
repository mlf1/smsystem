# oscm_app

from django.conf import settings


def getAttr(name):
	"""
	Gets the attribute from settings file given the name.
	"""
	"""
	TODO: generate an error message if the parameter doesn't exist in the the settings file.
	"""
	return getattr(settings, name)