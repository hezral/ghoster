#!/usr/bin/env python3

'''
   Copyright 2020 Adi Hezral (hezral@gmail.com) (https://github.com/hezral)

   This file is part of Ghoster ("Application").

    The Application is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    The Application is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this Application.  If not, see <http://www.gnu.org/licenses/>.
'''

# base imports
import sys, os

# gtk imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk, GObject


from datetime import datetime

print(datetime.now(), "python_run", )

# Ghoster imports
from main_window import GhosterWindow
from app_manager import AppManager


#------------------CLASS-SEPARATOR------------------#

class GhosterApp(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set application properties
        self.props.application_id = "com.github.hezral.ghoster"

        # initialize objects
        self.window = None
 
        self.app_manager = AppManager(gtk_application=self)

        print(datetime.now(), "app init")

    def do_startup(self):
        Gtk.Application.do_startup(self)

        # setup quiting app using Escape, Ctrl+Q
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_action)
        self.add_action(quit_action)
        self.set_accels_for_action("app.quit", ["<Ctrl>Q", "Escape"])

        # set dark theme since workspaces-view will rely on dark mode colors. 
        Gtk.Settings.get_default().set_property("gtk-application-prefer-dark-theme", True)
        
        # set CSS provider
        provider = Gtk.CssProvider()
        provider.load_from_path("data/application.css")
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        print(datetime.now(), "startup")

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if self.window is None:
            # Windows are associated with the application 
            # when the last one is closed the application shuts down
            self.window = GhosterWindow(application=self)
            self.add_window(self.window)
            self.window.show_all()

    def on_quit_action(self, action, param):
        if self.window is not None:
            self.window.destroy()


#------------------CLASS-SEPARATOR------------------#

if __name__ == "__main__":
    app = GhosterApp()
    app.run(sys.argv)


