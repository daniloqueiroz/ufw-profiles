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
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gobject
import pynotify
dbus.set_default_main_loop(DBusGMainLoop())


class NotificationListener(object):
    DBUS_INTERFACE = "bz.ufwprofiles.Manager"
    DBUS_SIGNAL = "ufw_profile_message"

    def __init__(self, bus):
        bus.add_signal_receiver(
            self.on_notification_send,
            dbus_interface=NotificationListener.DBUS_INTERFACE,
            signal_name=NotificationListener.DBUS_SIGNAL)

    def on_notification_send(self, message):
        notifications = pynotify.Notification("UFW Profiles", message)
        notifications.show()


if __name__ == '__main__':
    bus = dbus.SystemBus()
    loop = gobject.MainLoop()

    pynotify.init("ufw-profiles-notifies")
    NotificationListener(bus)

    loop.run()
