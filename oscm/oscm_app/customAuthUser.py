# oscm_app

from django.utils.translation import ugettext as _
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser

from .utils import getAttr
from oscm_app.authentication.customAuthUserManager import CustomAuthUserManager


"""
This class has been created to replace the standard user by adding some parameters ("Role", "Language", "Authentication"), to change the authentication mode if necessary and to choose the registration mode (by the admin via the admin interface, by the user via the registration interface and by the both persons via the both interfaces) too.
"""
class CustomAuthUser(AbstractBaseUser, PermissionsMixin):
	"""
	A fully featured User model with admin-compliant permissions.
	Username, email, role and language are required.
	"""

	# 'Only alphanumeric characters are allowed.'
	alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message=_('oscm_admin_usernameValidatorOfUser'))

	# Redefine the basic fields that would normally be defined in User
	# 'username'
	username = models.CharField(verbose_name=_('oscm_admin_usernameOfUser'), unique=True, max_length=30, validators=[alphanumeric])
	# 'email address'
	email = models.EmailField(verbose_name=_('oscm_admin_emailAddressOfUser'), unique=True, max_length=75)
	# 'first name'
	first_name = models.CharField(verbose_name=_('oscm_admin_firstNameOfUser'), max_length=30, null=True, blank=True)
	# 'last name'
	last_name = models.CharField(verbose_name=_('oscm_admin_lastNameOfUser'), max_length=30, null=True, blank=True)
	# 'date joined'
	date_joined = models.DateTimeField(verbose_name=_('oscm_admin_dateJoinedOfUser'), default=timezone.now)
	# 'active status'
	"""
	'Designates whether this user should be treated as 'active'. Unselect this instead of deleting accounts.'
	"""
	is_active = models.BooleanField(verbose_name=_('oscm_admin_activeStatusOfUser'), default=False, null=False, help_text=_('oscm_admin_helpTextActiveStatusOfUser'))
	# 'staff status'
	"""
	'Designates whether the user can log into this admin 'site'.'
	"""
	is_staff = models.BooleanField(verbose_name=_('oscm_admin_staffStatusOfUser'), default=False, null=False, help_text=_('oscm_admin_helpTextStaffStatusOfUser'))

	# Our own fields
	# Default parameter for the role attribute
	DEFAULT_ROLE = getAttr('DEFAULT_ROLE')
	# Retrieved the different roles from the settings file
	ROLE_CHOICES = getAttr('USER_ROLES')
	# Default parameter for the language attribute
	DEFAULT_LANGUAGE = getAttr('LANGUAGE_CODE')
	# Retrieved the different languages from the settings file
	LANGUAGE_CHOICES = getAttr('LANGUAGES')
	# Default parameter for the authentication attribute
	DEFAULT_AUTHENTICATION_MODE = getAttr('DEFAULT_AUTHENTICATION_MODE')
	# Retrieved the different authentications from the settings file
	AUTHENTICATION_MODE_CHOICES = getAttr('USER_AUTHENTICATION_MODES')


	# Added "role" attribute (from the settings file)
	role = models.CharField(max_length=7, 
		verbose_name=_('oscm_admin_roleOfUser'), 
		choices=ROLE_CHOICES, 
		default=DEFAULT_ROLE,
		help_text=_('oscm_admin_helpTextRoleOfUser')) 
	# Added "language" attribute (from the settings file)
	language = models.CharField(max_length=3, 
		verbose_name=_('oscm_admin_languageOfUser'), 
		choices=LANGUAGE_CHOICES, 
		default=DEFAULT_LANGUAGE,
		help_text=_('oscm_admin_helpTextLanguageOfUser'))
	# Added "authentication_mode" attribute (from the settings file)
	authentication_mode = models.CharField(max_length=10, 
		verbose_name=_('oscm_admin_authenticationModeOfApplication'), 
		choices=AUTHENTICATION_MODE_CHOICES, 
		default=DEFAULT_AUTHENTICATION_MODE, 
		help_text=_('oscm_admin_helpTextAuthenticationModeOfApplication'),
	)

	# Used the custom manager
	objects = CustomAuthUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email', 'role', 'language']

	class Meta:
		verbose_name = _('oscm_admin_headerOfOSCMUser')
		verbose_name_plural = _('oscm_admin_headerOfOSCMUsers')

	def get_full_name(self):
		"""
		Returns the first_name plus the last_name, with a space in between.
		"""
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		"""
		Returns the username for the user.
		"""
		return self.username

	def email_user(self, subject, message, from_email=None, **kwargs):
		"""
		Sends an email to this user.
		"""
		send_mail(subject, message, from_email, [self.email], **kwargs)

	def __str__(self):
		"""
		Displays the username, the email, the role and the language.
		"""
		return "{0} {1} {2} {3}".format(self.username, self.email, self.role, self.language)