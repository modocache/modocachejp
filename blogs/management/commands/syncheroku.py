from __future__ import print_function
import sys
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


HEROKU_CHECK_CMD = 'heroku version'
HEROKU_CONFIG_CMD = 'heroku config'
HEROKU_CONFIG_ADD_CMD = 'heroku config:add'


class Command(BaseCommand):
    help = 'Checks heroku config for settings.HEROKU_ENV_KEYS'
    verbose = False

    def _is_python3(self):
        return sys.version_info[0] >= 3

    def _msg(self, s, *args, **kwargs):
        print('{0}: {1}'.format('manage.py syncheroku', s), *args, **kwargs)

    def _heroku_available(self):
        cmd = HEROKU_CHECK_CMD
        if not self.verbose:
            cmd += ' &> /dev/null'
        else:
            self._msg('Checking for heroku gem...')
        try:
            subprocess.check_call(cmd, shell=True)
        except subprocess.CalledProcessError:
            return False
        return True

    def _prompt_for_input(self, key):
        """
        Prompt to add heroku config value for key.
        Returns value if not falsy, else None.
        """
        self._msg(
            'Set a value for {0}, or nothing to leave it blank: '.format(key),
            end=''
        )
        if self._is_python3():
            val = input()
        else:
            val = raw_input()
        return val

    def _get_heroku_config(self):
        """
        Return a dictionary contrining the key-value
        pairs shown by running 'heroku config'.
        """
        if self.verbose:
            self._msg("Checking heroku config...")
        config = {}
        raw = subprocess.check_output(
            'heroku config', stderr=subprocess.STDOUT, shell=True)
        keyvals = [e for e in raw.split() if e != '=>']
        for i in range(0, len(keyvals)-1, 2):
            config[keyvals[i]] = keyvals[i+1]

        if self.verbose:
            self._msg(config)

        return config

    def _get_unset_config_keys(self):
        """Return list of keys not set in heroku config."""
        config = self._get_heroku_config()
        return [k for k in settings.HEROKU_NECESSARY_ENVKEYS
                    if k not in config]

    def _heroku_config_add(self, config_dict):
        """Add a dictionary of key-value pairs to heroku config."""
        if not config_dict: return

        cmd = HEROKU_CONFIG_ADD_CMD
        for k, v in config_dict.items():
            cmd += ' {0}={1} '.format(k, v)
        subprocess.call(cmd, shell=True)

    def handle(self, *args, **options):
        """
        Iterate over unset heroku config keys,
        prompting user to set values. Config is updated
        if new values have been added.
        """
        self.verbose = int(options.get('verbosity')) > 1

        if not self._heroku_available():
            raise CommandError(
                'heroku gem does not appear to be installed. '
                'You can install the gem using the command '
                '`gem install heroku`.'
            )

        if self.verbose:
            self._msg('-'*50)

        to_add = {}
        for k in self._get_unset_config_keys():
            v = self._prompt_for_input(k)
            if v:
                to_add[k] = v
        self._heroku_config_add(to_add)

        if self.verbose:
            self._msg('Heroku config check done.')
            self._msg('-'*50)
