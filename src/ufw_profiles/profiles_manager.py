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
import logging
from os import devnull
from subprocess import call
from NetworkManager import NetworkManager
from ufw_profiles.commons import show_notification, ConfigManager

logger = logging.getLogger(__name__)


class UFWException(Exception):
    def __init__(self, command):
        self.command = command


class ProfileLoader(object):
    UFW_RESET_COMMAND = 'ufw --force reset'
    UFW_ENABLE_COMMAND = 'ufw enable'
    UFW_DEFAULT_COMMAND = 'ufw default deny'
    UFW_LOG_COMMAND = 'ufw logging low'

    def reload(self):
        connection_name = self._get_connection_name()
        try:
            logger.info("Reseting Firewall")
            self._reset_firewall()
            if connection_name:
                profile_name = ConfigManager.get_profile_for(connection_name)
                logger.info("Loading profile %s for network %s",profile_name,
                            connection_name)
                self._load_profile(profile_name)
        except (UFWException, IOError):
            logger.error("Error activating profile for %s", connection_name)
            # send notification
            show_notification("Error loading UFW profile")
            raise
        else:
            if connection_name:
                # send notification
                show_notification("Profile '%s' for network '%s' loaded" %
                                  (profile_name, connection_name))

    def _get_connection_name(self):
        name = None
        connections = NetworkManager.ActiveConnections
        if len(connections):
            name = 'wired'
            for connection in connections:
                if hasattr(connection.SpecificObject, 'Ssid'):
                    name = connection.SpecificObject.Ssid
        return name

    def _execute_ufw_command(self, command):
        with open(devnull, "w") as fnull:
            failed = call(command.split(),
                          stdout=fnull,
                          stderr=fnull)
        if failed:
            raise UFWException(command)

    def _reset_firewall(self):
        self._execute_ufw_command(ProfileLoader.UFW_RESET_COMMAND)
        self._execute_ufw_command(ProfileLoader.UFW_ENABLE_COMMAND)
        self._execute_ufw_command(ProfileLoader.UFW_DEFAULT_COMMAND)
        self._execute_ufw_command(ProfileLoader.UFW_LOG_COMMAND)

    def _load_profile(self, profile_name):
        rules = ConfigManager.get_rules_for(profile_name)
        for rule in rules:
            if not rule.startswith('#'):
                rule = 'ufw %s' % rule
                self._execute_ufw_command(rule)

