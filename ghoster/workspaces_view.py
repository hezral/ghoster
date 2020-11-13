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
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gdk, Granite


#------------------CLASS-SEPARATOR------------------#


class WorkspacesView(Gtk.Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        display = Gdk.Display.get_default()
        monitor = display.get_primary_monitor()
        geo = monitor.get_geometry()
        print(geo.width, geo.height)
        print(int(geo.width / 5), int(geo.height / 5))

        #-- WorkspacesView construct--------#
        self.props.name = 'workspaces-view'
        self.get_style_context().add_class(self.props.name)
        self.props.visible = True
        self.props.expand = True
        self.props.margin = 20
        self.props.margin_top = 12
        self.props.row_spacing = 20
        self.props.column_spacing = 6
        self.props.valign = Gtk.Align.CENTER


        box1 = WorkspaceBox()
        box2 = WorkspaceBox()

        stack = Gtk.Stack()
        stack.props.name = "workspaceview-stack"
        stack.props.transition_type = Gtk.StackTransitionType.SLIDE_LEFT_RIGHT
        stack.props.transition_duration = 750
        stack.add_named(box1, "box1")
        stack.add_named(box2, "box2")
        stack.show_all()

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.props.homogeneous = True
        stack_switcher.props.stack = stack
        stack_switcher.set_size_request(-1, 24)

        self.attach(stack, 0, 1, 1, 1)
        self.attach(stack_switcher, 0, 2, 1, 1)


class WorkspaceBox(Gtk.Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app1 = AppContainer("app1")
        d1 = WorkspaceArea()

        layout = Gtk.Layout()
        layout.set_size_request(300, 200)
        layout.props.expand = True
        layout.props.halign = layout.props.valign = Gtk.Align.FILL
        layout.props.margin = 25
        layout.add(app1)


        self.props.name = "Workspace 1"
        self.props.expand = True
        self.props.halign = self.props.valign = Gtk.Align.CENTER

        self.attach(layout, 0, 1, 1, 1)
        self.attach(d1, 0, 1, 1, 1)

        
        


class AppContainer(Gtk.Button):
    def __init__(self, name, iconsize=Gtk.IconSize.DIALOG, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.props.name = name
        self.props.image = Gtk.Image().new_from_icon_name("com.github.hezral.inspektor", iconsize)
        self.props.always_show_image = True
        self.props.expand = False
        self.props.halign = self.props.valign = Gtk.Align.CENTER
        self.props.margin = 2
        self.get_style_context().add_class("appcontainer")
        self.connect("realize", self.on_realize)

    def on_realize(self, *args):
        #print(locals())
        layout = self.get_parent()
        print(layout.get_allocation().x)
        print(layout.get_allocation().y)
        layout.move(self, 50, 50)



class WorkspaceArea(Gtk.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.props.name = "workspace-area"

        drawing_area = Gtk.DrawingArea()
        drawing_area.props.expand = True
        drawing_area.props.halign = self.props.valign = Gtk.Align.FILL
        #drawing_area.props.margin = 25
        drawing_area.set_size_request(384, 240)      

        drawing_area.connect("draw", self.draw)

        self.add(drawing_area)

    def draw(self, drawing_area, cairo_context):

        WORKSPACE_RADIUS = 4

        #print(locals())
        DOCK_WIDTH = 120
        DOCK_HEIGHT = 10
        DOCK_RADIUS = 3

        PANEL_HEIGHT = 8
        PLUS_SIZE = 70
        PLUS_WIDTH = 10


        OVERLAY_COLOR = Gdk.RGBA(red=252 / 255.0, green=245 / 255.0, blue=213 / 255.0, alpha=0.35)
        height = drawing_area.get_allocated_height()
        width = drawing_area.get_allocated_width()

        cairo_context.set_source_rgba(OVERLAY_COLOR.red, OVERLAY_COLOR.green, OVERLAY_COLOR.blue, OVERLAY_COLOR.alpha)

        # window
        Granite.DrawingUtilities.cairo_rounded_rectangle(cairo_context, 0, 0, width, height, WORKSPACE_RADIUS)
        cairo_context.clip()
        cairo_context.set_line_width(4)
        Granite.DrawingUtilities.cairo_rounded_rectangle(cairo_context, 0, 0, width, height, WORKSPACE_RADIUS)
        cairo_context.stroke()

        # wingpanel
        cairo_context.set_source_rgba(OVERLAY_COLOR.red, OVERLAY_COLOR.green, OVERLAY_COLOR.blue, 0.5)
        cairo_context.rectangle (0, 0, width, PANEL_HEIGHT)
        cairo_context.fill()

        # plank
        Granite.DrawingUtilities.cairo_rounded_rectangle(cairo_context, (width - DOCK_WIDTH) / 2, height - DOCK_HEIGHT, DOCK_WIDTH, DOCK_HEIGHT + DOCK_RADIUS, DOCK_RADIUS)
        cairo_context.fill()

