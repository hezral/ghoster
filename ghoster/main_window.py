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


import sys, os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gio, Gdk, Granite, GObject, Pango

# Ghoster imports
from settings_view import SettingsView
from workspaces_view import WorkspacesView


#------------------CLASS-SEPARATOR------------------#


class GhosterWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #-- view --------#
        workspaces_view = WorkspacesView()
        settings_view = SettingsView()
        settings_view.connect("notify::visible", self.on_view_visible)
        
        #-- stack --------#
        stack = Gtk.Stack()
        stack.props.transition_type = Gtk.StackTransitionType.CROSSFADE
        stack.add_named(settings_view, settings_view.get_name())
        stack.add_named(workspaces_view, workspaces_view.get_name())
        
        #-- header --------#
        word_label = Gtk.Label("Ghoster")
        word_label.props.vexpand = True
        word_label.get_style_context().add_class("lookup-word-header")

        edit_img = Gtk.Image().new_from_icon_name("insert-text-symbolic", Gtk.IconSize.SMALL_TOOLBAR)
        edit_img.props.no_show_all = True
        edit_img.get_style_context().add_class("transition-on")

        word_grid = Gtk.Grid()
        word_grid.props.column_spacing = 4
        word_grid.props.halign = Gtk.Align.START
        word_grid.props.valign = Gtk.Align.CENTER
        word_grid.attach(word_label, 0, 1, 1, 1)
        word_grid.attach(edit_img, 1, 1, 1, 1)

        word_box = Gtk.EventBox()
        word_box.add(word_grid)

        #------ view switch ----#
        icon_theme = Gtk.IconTheme.get_default()
        icon_theme.prepend_search_path("data/icons")
        view_switch = Granite.ModeSwitch.from_icon_name("com.github.hezral.quickwork-symbolic", "preferences-system-symbolic")
        view_switch.props.primary_icon_tooltip_text = "Word Lookup"
        view_switch.props.secondary_icon_tooltip_text = "Settings"
        view_switch.props.valign = Gtk.Align.CENTER
        view_switch.bind_property("active", settings_view, "visible", GObject.BindingFlags.BIDIRECTIONAL)

        #-- header construct--------#
        headerbar = Gtk.HeaderBar()
        headerbar.pack_start(word_box)
        headerbar.pack_end(view_switch)
        headerbar.props.show_close_button = False
        headerbar.props.decoration_layout = "close:maximize"
        headerbar.get_style_context().add_class("default-decoration")
        headerbar.get_style_context().add_class(Gtk.STYLE_CLASS_FLAT)

        #-- GhosterWindow construct--------#
        self.props.resizable = False #set this and window will expand and retract based on child
        self.title = "Ghoster"
        self.set_keep_above(True)
        self.get_style_context().add_class("rounded")
        self.set_size_request(650, 550) #set width to -1 to expand and retract based on content
        self.props.window_position = Gtk.WindowPosition.CENTER_ALWAYS
        self.set_titlebar(headerbar)
        self.add(stack)
        
        #-- GhosterWindow variables and settings--------#
        self.on_start_variables()
        self.on_start_settings()
        self.lookup_word = "Ghoster"
        self.active_view = workspaces_view

    def on_start_variables(self):
        # this is for tracking window state flags for persistent mode
        self.state_flags_changed_count = 0
        self.active_state_flags = ['GTK_STATE_FLAG_NORMAL', 'GTK_STATE_FLAG_DIR_LTR']

    def on_start_settings(self):
        # read user saved settings
        gio_settings = Gio.Settings(schema_id="com.github.hezral.ghoster")

        if gio_settings.get_value("first-run"):
            self.first_run = True
            print("first-run")
        

    def get_window_child_widgets(self):
        window = self
        window_children = window.get_children()
        headerbar = [child for child in window_children if isinstance(child, Gtk.HeaderBar)][0]
        stack = [child for child in window_children if isinstance(child, Gtk.Stack)][0]
        word_box = [child for child in headerbar.get_children() if isinstance(child, Gtk.EventBox)][0]
        word_grid = word_box.get_child()
        return headerbar, stack, word_grid

    def get_window_child(self, class_obj):
        widget = [child for child in self.get_children() if isinstance(child, class_obj)][0]
        return widget
            
    def on_view_visible(self, view, gparam=None, runlookup=None, word=None):
        headerbar, stack, word_grid = self.get_window_child_widgets()
        word_label = [child for child in word_grid.get_children() if isinstance(child, Gtk.Label)][0]
        workspaces_view = stack.get_child_by_name("workspaces-view")
        settings_view = stack.get_child_by_name("settings-view")

        if word is not None:
            self.lookup_word = word.capitalize()

        # toggle settings-view visibility based on visible property
        if view.props.name == "settings-view" and view.is_visible():
            # view.show_all() # have to manually show settings-view?
            self.active_view = settings_view
            word_label.props.label = "Settings"

        else:
            view.hide()
            self.active_view = workspaces_view
            word_label.props.label = "Ghoster"

        # toggle css styling
        if self.active_view.props.name == "settings-view":
            stack.get_style_context().add_class("stack-settings")
            headerbar.get_style_context().add_class("headerbar-settings")
        else:
            stack.get_style_context().remove_class("stack-settings")
            headerbar.get_style_context().remove_class("headerbar-settings")

        # finally set visible stack
        stack.set_visible_child_name(name=self.active_view.props.name)


    def on_persistent_mode(self, widget, event):
        # state flags for window active state
        self.state_flags = self.get_state_flags().value_names
        # print(self.state_flags)
        if not self.state_flags == self.active_state_flags and self.state_flags_changed_count > 1:
            self.destroy()
        else:
            self.state_flags_changed_count += 1
            # print('state-flags-changed', self.state_flags_changed_count)

