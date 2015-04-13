# oscm_app/management/commands

import sys
import getpass

from optparse import make_option

from django.core.management.base import (BaseCommand, CommandError)
from django.contrib.auth import get_user_model
from django.contrib.auth.management import get_default_username
from django.utils import translation
from django.db import DEFAULT_DB_ALIAS
from django.utils.text import capfirst
from django.utils.encoding import force_str
from django.core import exceptions


class NotRunningInTTYException(BaseException):
    pass


class Command(BaseCommand):

    """
    Management utility to create OSCM superusers.
    """

    # A short description of the command
    help = 'Create an OSCM superuser'
    """
    A boolean indicating whether the command needs to be able
    to import Django settings
    """
    can_import_settings = True

    def __init__(self, *args, **kwargs):
        """
        Options are defined in an __init__ method to support
        swapping out custom user models in tests.
        """
        super(Command, self).__init__(*args, **kwargs)
        # Retrieve the custom model auth
        self.UserModel = get_user_model()
        self.username_field = self.UserModel._meta.get_field(
            self.UserModel.USERNAME_FIELD)

        # Options list
        self.option_list = BaseCommand.option_list + (
            make_option(
                '--%s' % self.UserModel.USERNAME_FIELD,
                dest=self.UserModel.USERNAME_FIELD, default=None,
                help='Specifies the login for the OSCM superuser.'),
            make_option(
                '--noinput',
                action='store_false',
                dest='interactive',
                default=True,
                help=(
                    "Tells Django to NOT prompt the user for input of any "
                    "kind. You must use --%s with --noinput, along with an "
                    "option for any other required field. OSCM superuser "
                    "created with --noinput will not be able to log in until "
                    "they\'re given a valid password."
                    % self.UserModel.USERNAME_FIELD)),
            make_option(
                '--database',
                action='store',
                dest='database',
                default=DEFAULT_DB_ALIAS,
                help='Specifies the database to use. Default is "default".'),
        ) + tuple(
            make_option(
                '--%s' % field,
                dest=field,
                default=None,
                help='Specifies the %s for the OSCM superuser.' % field)
            for field in self.UserModel.REQUIRED_FIELDS)

    option_list = BaseCommand.option_list

    def execute(self, *args, **options):
        """
        Execute the command line.
        """
        # Used for testing
        self.stdin = options.get('stdin', sys.stdin)
        return super(Command, self).execute(*args, **options)

    def handle(self, *args, **options):
        """
        Check the parameters and do the job.
        """
        from django.conf import settings
        translation.activate(settings.LANGUAGE_CODE)

        username = options.get(self.UserModel.USERNAME_FIELD, None)
        interactive = options.get('interactive')
        verbosity = int(options.get('verbosity', 1))
        database = options.get('database')

        # If not provided, create the user with an unusable password
        password = None
        user_data = {}

        # Do quick and dirty validation if --noinput
        if not interactive:
            try:
                if not username:
                    raise CommandError(
                        'You must use --%s with --noinput.'
                        % self.UserModel.USERNAME_FIELD)
                username = self.username_field.clean(username, None)

                for field_name in self.UserModel.REQUIRED_FIELDS:
                    if options.get(field_name):
                        field = self.UserModel._meta.get_field(field_name)
                        user_data[field_name] = field.clean(
                            options[field_name], None)
                    else:
                        raise CommandError(
                            "You must use --%s with --noinput." % field_name)
            except exceptions.ValidationError as validation_error:
                raise CommandError('; '.join(validation_error.messages))
        else:
            # Prompt for username/password, and any other required fields.
            # Enclose this whole thing in a try/except to trap for a
            # keyboard interrupt and exit gracefully.
            default_username = get_default_username()
            try:
                if hasattr(self.stdin, 'isatty') and not self.stdin.isatty():
                    raise NotRunningInTTYException("Not running in a TTY")

                # Get a username
                verbose_field_name = self.username_field.verbose_name
                while username is None:
                    if not username:
                        input_msg = capfirst(verbose_field_name)
                        if default_username:
                            input_msg = (
                                "%s (leave blank to use '%s'"
                                ")" % (input_msg, default_username))
                        raw_value = input(force_str('%s: ' % input_msg))
                    if default_username and raw_value == '':
                        raw_value = default_username
                    try:
                        username = self.username_field.clean(raw_value, None)
                    except exceptions.ValidationError as validation_error:
                        self.stderr.write("Error: %s" % '; '.join(
                            validation_error.messages))
                        username = None
                        continue
                    try:
                        self.UserModel._default_manager.db_manager(
                            database).get_by_natural_key(username)
                    except self.UserModel.DoesNotExist:
                        pass
                    else:
                        self.stderr.write(
                            "Error: That %s is already taken, please select "
                            "another." % verbose_field_name)
                        username = None

                # Retrieve required parameters and check them
                for field_name in self.UserModel.REQUIRED_FIELDS:
                    field = self.UserModel._meta.get_field(field_name)
                    user_data[field_name] = options.get(field_name)
                    while user_data[field_name] is None:
                        if field.choices:
                            choices = force_str(
                                '%s choices:'
                                '\n' % capfirst(field.verbose_name))
                            index = 0
                            for key, value in field.choices:
                                index += 1
                                choices += '\n'.join(
                                    [' %s --> %s (%s)\n' % (
                                        index, value, key)])
                            val = input('%s %s: ' % (
                                force_str(choices),
                                capfirst(field.verbose_name)))
                            if val == '':
                                self.stderr.write(
                                    "Invalid choice: empty value. Select a "
                                    "valid choice.")
                                user_data[field_name] = None
                                continue
                            try:
                                if (int(val) < 1
                                        or int(val) > len(field.choices)):
                                    self.stderr.write(
                                        "Invalid choice: select a valid "
                                        "choice between 1 and %d. \'%s\' in "
                                        "not one of the available choices"
                                        "." % (len(field.choices), val))
                                    user_data[field_name] = None
                                    continue
                                raw_value = field.choices[(int(val) - 1)][0]
                            except (ValueError, IndexError):
                                self.stderr.write(
                                    "Invalid choice: select a valid choice. "
                                    "\'%s\' in not one of the available "
                                    "choices." % val)
                                user_data[field_name] = None
                                continue
                        else:
                            raw_value = input(force_str(
                                '%s: ' % capfirst(field.verbose_name)))
                        try:
                            user_data[field_name] = field.clean(
                                raw_value, None)
                        except exceptions.ValidationError as validation_error:
                            self.stderr.write(
                                "Error: %s" % '; '.join(
                                    validation_error.messages))
                            user_data[field_name] = None
                            continue
                        if field.unique:
                            if field_name == 'email':
                                try:
                                    (
                                        self.UserModel._default_manager.
                                        db_manager(database).
                                        get(email=raw_value))
                                except self.UserModel.DoesNotExist:
                                    pass
                                else:
                                    self.stderr.write(
                                        "Error: That %s is already taken, "
                                        "please select "
                                        "another." % field.verbose_name)
                                    user_data[field_name] = None
                            else:
                                self.stderr.write(
                                    "Error: That %s hasn't specific "
                                    "validation." % verbose_field_name)
                                user_data[field_name] = None

                # Get a password
                while password is None:
                    if not password:
                        password = getpass.getpass()
                        password2 = getpass.getpass(
                            force_str('Password (again): '))
                        if password != password2:
                            self.stderr.write(
                                "Error: Your passwords didn't match.")
                            password = None
                            continue
                    if password.strip() == '':
                        self.stderr.write(
                            "Error: Blank passwords aren't allowed.")
                        password = None
                        continue

            except KeyboardInterrupt:
                self.stderr.write("\nOperation cancelled.")
                sys.exit(1)

            except NotRunningInTTYException:
                self.stderr.write(
                    "OSCM superuser creation skipped due to not running in a "
                    "TTY. You can run `manage.py createoscmsuperuser` in "
                    "your project to create one manually."
                )

        if username:
            user_data[self.UserModel.USERNAME_FIELD] = username
            user_data['password'] = password
            self.UserModel._default_manager.db_manager(
                database).create_superuser(**user_data)
            if verbosity >= 1:
                self.stdout.write("OSCM superuser created successfully.")

        translation.deactivate()
