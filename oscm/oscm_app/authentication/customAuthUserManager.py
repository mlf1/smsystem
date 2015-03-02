# oscm_app/authentication

from django.contrib.auth.models import BaseUserManager


class CustomAuthUserManager(BaseUserManager):

	def create_user(self, username, email, role, language, is_staff, is_superuser, password=None):
		"""
		Creates and saves a User with the given username, email, role, language and password.
		"""
		if not email:
			# 'Users must have an email address.'
			raise ValidationError(_('Missing email address: %(value)s'), 
				code='missing', 
				params={'value': email},)
		if not username:
			# 'Users must have an username.'
			raise ValidationError(_('Missing username: %(value)s'), 
				code='missing', 
				params={'value': username},)
		if not role:
			# 'Users must have a specific role.'
			raise ValidationError(_('Missing role: %(value)s'), 
				code='missing', 
				params={'value': role},)
		if not language:
			# 'Users must have a specific language.'
			raise ValidationError(_('Missing language: %(value)s'), 
				code='missing', 
				params={'value': language},)
		email = self.normalize_email(email)
		customUser = self.model(username=username, email=email, role=role, language=language, is_staff=is_staff, is_superuser=is_superuser)
		customUser.set_password(password)
		customUser.save(using=self._db)
		return customUser

	def create_superuser(self, username, email, role, language, password):
		"""
		Creates and saves a super User with the given username, email, role,language and password.
		"""
		customUser = self.create_user(username=username, email=email, role=role, language=language, is_staff=True, is_superuser=True, password=password)

		# Sets the 'is_active' attribute to 'True'
		customUser.is_active = True
		customUser.save(using=self._db)
		return customUser