#! /usr/bin/env python
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
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gobject
dbus.set_default_main_loop(DBusGMainLoop())

from ufw_profiles.commons import ConfigManager, DbusConnector
from ufw_profiles.profiles_manager import ProfileLoader
from ufw_profiles.listeners import (ConnectionStateListener,
                                    ConfigurationModificationListener)


def reload_profile_callback(profile_loader):
    def callback():
        ConfigManager.reload()
        profile_loader.reload()
    return callback


if __name__ == '__main__':
    bus = dbus.SystemBus()
    loop = gobject.MainLoop()
    gobject.threads_init()

    logging.basicConfig(level=logging.INFO,
                        format=('%(asctime)s %(name)-12s %(levelname)-8s'
                                ' %(message)s'),
                        datefmt='%m-%d %H:%M',
                        filename='/var/log/ufw-profiles.log',
                        filemode='a')
    logger = logging.getLogger(__name__)
    logger.info("Starting UFW-Profiles daemon")
    dbus_connector = DbusConnector(bus)

    profile_loader = ProfileLoader(dbus_connector)
    handler = reload_profile_callback(profile_loader)
    ConnectionStateListener(bus, handler)
    files_listener = ConfigurationModificationListener(handler)
    handler()

    loop.run()
