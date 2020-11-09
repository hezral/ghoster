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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango


#------------------CLASS-SEPARATOR------------------#


class WorkspacesView(Gtk.Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #-- Ghoster logo --------#
        left_icon = Gtk.Image().new_from_file("data/icons/134.svg")
        #left_icon.get_style_context().add_class("Ghoster-icon-left")
        right_icon = Gtk.Image().new_from_file("data/icons/133.svg")
        right_icon.get_style_context().add_class("Ghoster-icon-right")
        icon_overlay = Gtk.Overlay()
        icon_overlay.add(left_icon)
        icon_overlay.add_overlay(right_icon)
        icon_overlay.props.can_focus = True
        icon_overlay.props.focus_on_click = True
        icon_overlay.grab_focus()
        
        #-- message header --------#
        message = Gtk.Label("No word detected")
        message.props.name = "message"
        message.props.margin_bottom = 5
        message.props.hexpand = True
        message.props.halign = Gtk.Align.CENTER
        message.props.valign = Gtk.Align.CENTER
        message.props.max_width_chars = 30
        message.props.wrap = True
        message.props.wrap_mode = Pango.WrapMode.WORD
        message.props.justify = Gtk.Justification.CENTER
        message.get_style_context().add_class("h3")

        #-- message header --------#
        sub_message = Gtk.Label("Select a word in any application or document\nor type a word below to get a quick word lookup")
        sub_message.props.margin_bottom = 10
        sub_message.props.hexpand = True
        sub_message.props.halign = Gtk.Align.CENTER
        sub_message.props.valign = Gtk.Align.CENTER
        sub_message.props.max_width_chars = 40
        sub_message.props.wrap = True
        sub_message.props.wrap_mode = Pango.WrapMode.WORD
        sub_message.props.justify = Gtk.Justification.CENTER


        #-- NoWordView construct--------#
        self.props.name = 'workspaces-view'
        self.get_style_context().add_class(self.props.name)
        self.props.visible = True
        self.props.expand = True
        self.props.margin = 20
        self.props.margin_top = 12
        self.props.row_spacing = 12
        self.props.column_spacing = 6
        self.props.valign = Gtk.Align.CENTER
        self.attach(icon_overlay, 0, 1, 1, 1)
        self.attach(message, 0, 2, 1, 1)
        self.attach(sub_message, 0, 3, 1, 1)




