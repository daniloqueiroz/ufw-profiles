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
from datetime import datetime, timedelta
import logging
import gobject
import pyinotify
from ufw_profiles.commons import CONFIG_DIR

logger = logging.getLogger(__name__)

class ConfigurationModificationListener(pyinotify.ProcessEvent):
    def __init__(self, handler):
        pyinotify.ProcessEvent.__init__(self)
        wm = pyinotify.WatchManager()
        wm.add_watch(CONFIG_DIR, pyinotify.IN_CLOSE_WRITE)
        notifier = pyinotify.ThreadedNotifier(
            wm, self)
        notifier.start()
        self._last_read = datetime.now()
        self._handler = handler

    def process_default(self, event):
        now = datetime.now()
        if self._last_read + timedelta(seconds=5) < now:
            logger.info("Configuration file changed, reloading UFW")
            self._last_read = now
            gobject.timeout_add(1000, self._handler)


class ConnectionStateListener(object):
    DBUS_INTERFACE = "org.freedesktop.NetworkManager"
    DBUS_SIGNAL = "PropertiesChanged"
    CONNECTED_STATE = 70
    DISCONNECTED_STATE = 20

    def __init__(self, bus, handler):
        self._handler = handler
        bus.add_signal_receiver(
            self.on_connection_changed,
            dbus_interface=ConnectionStateListener.DBUS_INTERFACE,
            signal_name=ConnectionStateListener.DBUS_SIGNAL)

    def on_connection_changed(self, *args, **keywords):
        state = args[0].get('State', -1)
        if (state == ConnectionStateListener.CONNECTED_STATE or
                state == ConnectionStateListener.DISCONNECTED_STATE):
            logger.info("Connection state changed, reloading UFW")
            self._handler()
