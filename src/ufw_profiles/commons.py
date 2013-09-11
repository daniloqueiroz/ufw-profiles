"""
UFW-profiles
Copyright (C) 2013  Danilo Queiroz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see [http://www.gnu.org/licenses/].
"""
from ConfigParser import RawConfigParser
import pynotify

CONFIG_DIR = '/etc/ufw/profiles'
_DEFAULT_PROFILE = 'default'
_PROFILES_SECTION = 'profiles'
_PROFILES_FILE = '%s/networks.conf' % CONFIG_DIR
_PROFILE_RULES_PATTERN = CONFIG_DIR + '/%s.rules'

pynotify.init("ufw-profiles")


def show_notification(message):
    notifications = pynotify.Notification("UFW Profiles", message)
    notifications.show()


class ConfigManager(object):
    _config = None

    @staticmethod
    def get_profile_for(connection_name):
        profile_name = _DEFAULT_PROFILE
        if ConfigManager._config.has_option(_PROFILES_SECTION,
                                            connection_name):
            profile_name = ConfigManager._config.get(_PROFILES_SECTION,
                                                     connection_name)
        return profile_name

    @staticmethod
    def get_rules_for(profile_name):
        profile_file = _PROFILE_RULES_PATTERN % profile_name
        with open(profile_file, 'r') as fd:
            lines = fd.readlines()
        return lines

    @staticmethod
    def reload():
        ConfigManager._config = RawConfigParser()
        ConfigManager._config.read(_PROFILES_FILE)

ConfigManager.reload()
