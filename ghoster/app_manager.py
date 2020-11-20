#!/usr/bin/env python3

'''
   Copyright 2020 Adi Hezral (hezral@gmail.com) (https://github.com/hezral)

   This file is part of Movens.

    Movens is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Movens is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Movens.  If not, see <http://www.gnu.org/licenses/>.
'''

import gi
gi.require_version('Gtk', '3.0')
gi.require_version("Bamf", "3")
gi.require_version("Wnck", "3.0")
from gi.repository import Gtk, Bamf, Wnck


# list of excluded apps by default
exclude_list = ('Wingpanel',
                'Plank',)

#------------------CLASS-SEPARATOR------------------#


class AppManager():
    
    screen = Wnck.Screen.get_default()
    matcher = Bamf.Matcher.get_default()

    def __init__(self, gtk_application, *args, **kwargs):

        self.screen.force_update()
        
        # create empty dictionary instaces for each workspace available
        # these will hold the apps info nested dictionary
        self.update_workspaces()

        # get all running applications
        self.update_running_apps()

        #self.on_events("startup")

        # setup signals
        self.screen.connect('application-opened', self.on_application_event, "app-open")
        self.screen.connect('application-closed', self.on_application_event, "app-close")
        self.screen.connect("workspace_created", self.on_workspace_event, "workspace-create")
        self.screen.connect("workspace_destroyed", self.on_workspace_event, "workspace-destroy")

    def update_workspaces(self):

        self.workspaces = {}
        self.workspaces.clear()

        for workspace in self.screen.get_workspaces():
            self.workspaces[workspace.get_number()] = {}

    def update_running_apps(self):
        """ get all running application and populate workspaces dictionary """

        for app in self.matcher.get_running_applications():
            if app.get_name() not in exclude_list:
                self.add_application_info(app)

    def add_application_info(self, bamf_application, event_type="startup"):
        """ get application info and add to workspaces dictionary based which workspace the app is in """

        name = bamf_application.get_name()

        for xid in bamf_application.get_xids():

            # xid = bamf_application.get_xids()[0]
            xid = xid
            desktop_file = bamf_application.get_desktop_file()
            
            # wnck_window = [window for window in self.screen.get_windows() if xid == window.get_xid()][0]
            # wnck_window.connect("workspace_changed", self.on_window_event, "window-workspace-changed")

            # for window in self.screen.get_windows():
            #     if xid == window.get_xid():
            #         print("window count", window.get_workspace().get_name(), window.get_name())

            for wnck_window in self.screen.get_windows():
                if xid == wnck_window.get_xid():

                    wnck_window.connect("workspace_changed", self.on_window_event, "window-workspace-changed")

                    wnck_wm_class_name = wnck_window.get_class_instance_name()
                    wnck_wm_class_group = wnck_window.get_class_group_name()

                    wnck_app = wnck_window.get_application()
                    wnck_xid = wnck_app.get_xid()
                    icon_pixbuf = wnck_app.get_icon() #gdkpixbuf
                    icon_name = bamf_application.get_icon() #str icon_name

                    if wnck_window.get_workspace() is not None:
                        workspace_n = wnck_window.get_workspace().get_number()
                        workspace_name = wnck_window.get_workspace().get_name()
                    else:
                        workspace_n = None
                        workspace_name = None
                    
                    if workspace_n is not None:
                        app_info = {
                                    "name": name, 
                                    "wnck_xid": wnck_xid, 
                                    "xid": xid, 
                                    "workspace_n": workspace_n, 
                                    "workspace_name": workspace_name, 
                                    "icon": icon_pixbuf, 
                                    "icon_name": icon_name, 
                                    "desktop_file": desktop_file,
                                    "wnck_wm_class_name": wnck_wm_class_name,
                                    "wnck_wm_class_group": wnck_wm_class_group
                                }

                        # add app to workspace dictionary using wnck_xid as key
                        self.workspaces[workspace_n][wnck_xid] = app_info

    def on_application_event(self, wnck_screen, wnck_application, event_type):

        if wnck_application.get_name().capitalize() not in exclude_list:
            
            #print(event_type)

            # if event_type == "open":
            #     # add app to workspaces dictionary
            #     for wnck_windows in wnck_application.get_windows():
            #         bamf_xid = wnck_windows.get_xid()
            #         bamf_application = self.matcher.get_application_for_xid(bamf_xid)

            #         self.add_application_info(bamf_application)

            #     # # add app to workspaces dictionary
            #     # wnck_windows = wnck_application.get_windows()
            #     # bamf_xid = wnck_windows[0].get_xid()
            #     # bamf_application = self.matcher.get_application_for_xid(bamf_xid)

            #     # self.add_application_info(bamf_application)

            # elif event_type == "close":
            #     # remove app from workspaces dictionary
            #     for workspace_number in self.workspaces.copy():
            #         for app_xid in self.workspaces[workspace_number].copy():
            #             if app_xid == wnck_application.get_xid():
            #                 del(self.workspaces[workspace_number][app_xid])
            #                 #print(self.workspaces[key][subkey]["name"])

            self.update_workspaces()
            self.update_running_apps()

            self.on_events(event_type)

    def on_workspace_event(self, wnck_screen, wnck_workspace, event_type):
        """ add/remove workspaces dictionary as signal triggered """
        #print(event_type)

        # if event_type == "create":
            
        #     if wnck_workspace.get_number() not in self.workspaces.keys():
        #         self.workspaces[wnck_workspace.get_number()] = {}
                
        # elif event_type == "destroy":

        #     if wnck_workspace.get_number() in self.workspaces.keys():
        #         del(self.workspaces[wnck_workspace.get_number()])
        
        self.update_workspaces()
        self.update_running_apps()

        #self.on_events(event_type)


    def on_window_event(self, wnck_window, event_type):
        print(event_type)

        self.update_workspaces()
        self.update_running_apps()

        #self.on_events(event_type)


    def on_events(self, event_type):
        # for debug
        print(event_type)
        for workspace_number in self.workspaces:
            for app_xid in self.workspaces[workspace_number]:
                print("Workspace:", workspace_number + 1, self.workspaces[workspace_number][app_xid]["name"], self.workspaces[workspace_number][app_xid]["wnck_wm_class_name"], self.workspaces[workspace_number][app_xid]["wnck_wm_class_group"])


apps_manager = AppManager(gtk_application=None)

from conf_manager import ConfigManager
configs_manager = ConfigManager(gtk_application=None)

import signal
from gi.repository import GLib
GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, Gtk.main_quit) 

Gtk.main()