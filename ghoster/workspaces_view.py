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
from gi.repository import Gtk, Gdk, Granite, GObject

#------------------CONSTANTS------------------#

WORKSPACE_WIDTH = 384
WORKSPACE_HEIGHT = 250
WORKSPACE_RADIUS = 4

DOCK_WIDTH = 120
DOCK_HEIGHT = 10
DOCK_RADIUS = 3

PANEL_HEIGHT = 8

OVERLAY_COLOR = Gdk.RGBA(red=252 / 255.0, green=245 / 255.0, blue=213 / 255.0, alpha=0.35)


#------------------CLASS-SEPARATOR------------------#


class WorkspacesView(Gtk.Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add custom signals for callback AppManager if application_opened/closed events are triggered
        # GObject.signal_new(signal_name, type, flags, return_type, param_types)
        # param_types is a list example [GObject.TYPE_PYOBJECT, GObject.TYPE_STRING]
        GObject.signal_new("on-workspace-view-event", Gtk.Grid, GObject.SIGNAL_RUN_LAST, GObject.TYPE_BOOLEAN, [GObject.TYPE_PYOBJECT])

        display = Gdk.Display.get_default()
        monitor = display.get_primary_monitor()
        geo = monitor.get_geometry()
        print(geo.width, geo.height)
        print(int(geo.width / 5), int(geo.height / 5))

        #-- WorkspacesView construct--------#
        self.props.name = "workspaces-view"
        self.get_style_context().add_class(self.props.name)
        #self.props.visible = True
        self.props.expand = True
        self.props.margin = 20
        # self.props.margin_top = 12
        self.props.row_spacing = 15
        self.props.column_spacing = 6
        #self.props.valign = Gtk.Align.CENTER
        self.connect("on-workspace-view-event", self.on_workspace_view_event)


        box1 = WorkspaceBox("app1", "Workspace 1")
        box2 = WorkspaceBox("app2", "Workspace 2")

        stack = Gtk.Stack()
        stack.props.name = "workspaceview-stack"
        stack.props.transition_type = Gtk.StackTransitionType.SLIDE_LEFT_RIGHT
        stack.props.transition_duration = 750
        stack.add_named(box1, "box1")
        stack.add_named(box2, "box2")

        # Use icon instead for stack switcher
        for child in stack.get_children():
            stack.child_set_property(child, "icon-name", "user-offline")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.props.homogeneous = False
        stack_switcher.props.expand = False
        stack_switcher.props.halign = Gtk.Align.CENTER
        stack_switcher.props.stack = stack
        stack_switcher.set_size_request(-1, 24)
        stack_switcher.get_style_context().add_class("workspaces-switcher")

        # add tooltip text to stack switcher buttons
        for child in stack_switcher.get_children():
            child.props.has_tooltip = True
            child_index = stack_switcher.get_children().index(child)
            child.props.tooltip_text = stack.get_children()[child_index].props.name

        self.attach(stack, 0, 1, 1, 1)

        if len(stack.get_children()) > 1:
            self.attach(stack_switcher, 0, 2, 1, 1)

    def generate_view(self):
        pass
        

    def on_workspace_view_event(self):
        print(locals())

class WorkspaceBox(Gtk.Grid):
    def __init__(self, app_name, workspace_name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app1 = AppContainer(app_name)
        d1 = WorkspaceArea()

        layout = Gtk.Layout()
        layout.set_size_request(WORKSPACE_WIDTH, WORKSPACE_HEIGHT)
        layout.props.expand = True
        layout.props.halign = layout.props.valign = Gtk.Align.CENTER
        layout.add(app1)

        workspace_label = Gtk.Label(workspace_name)
        workspace_label.props.name = "workspace-name"

        self.props.name = workspace_name
        self.props.expand = True
        self.props.halign = self.props.valign = Gtk.Align.CENTER
        self.props.row_spacing = 20

        self.attach(layout, 0, 1, 1, 1)
        self.attach(d1, 0, 1, 1, 1)
        self.attach(workspace_label, 0, 2, 1, 1)

        #self.connect("map", self.on_map)
        

    def on_map(self, *args):
        print(locals())
        
        


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
        self.connect("map", self.on_realize)


    def on_realize(self, *args):
        #print(locals())
        layout = self.get_parent()
        print("x:",layout.get_allocation().x, " y:", layout.get_allocation().y)
        #layout.move(self, 0, 0)
        print(self.props.name, "x:",self.get_allocation().x, " y:", self.get_allocation().y)


class WorkspaceArea(Gtk.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.props.name = "workspace-area"

        drawing_area = Gtk.DrawingArea()
        drawing_area.props.expand = True
        drawing_area.props.halign = self.props.valign = Gtk.Align.FILL    

        drawing_area.connect("draw", self.draw)

        self.add(drawing_area)

    def draw(self, drawing_area, cairo_context):

        height = drawing_area.get_allocated_height()
        width = drawing_area.get_allocated_width()


        cairo_context.set_source_rgba(OVERLAY_COLOR.red, OVERLAY_COLOR.green, OVERLAY_COLOR.blue, OVERLAY_COLOR.alpha)

        # workspace area
        Granite.DrawingUtilities.cairo_rounded_rectangle(cairo_context, 0, 0, WORKSPACE_WIDTH, WORKSPACE_HEIGHT, WORKSPACE_RADIUS)
        cairo_context.clip()
        cairo_context.set_line_width(4)
        Granite.DrawingUtilities.cairo_rounded_rectangle(cairo_context, 0, 0, WORKSPACE_WIDTH, WORKSPACE_HEIGHT, WORKSPACE_RADIUS)
        cairo_context.stroke()

        # wingpanel
        cairo_context.set_source_rgba(OVERLAY_COLOR.red, OVERLAY_COLOR.green, OVERLAY_COLOR.blue, 0.5)
        cairo_context.rectangle (0, 0, width, PANEL_HEIGHT)
        cairo_context.fill()

        # plank
        Granite.DrawingUtilities.cairo_rounded_rectangle(cairo_context, (WORKSPACE_WIDTH - DOCK_WIDTH) / 2, WORKSPACE_HEIGHT - DOCK_HEIGHT, DOCK_WIDTH, DOCK_HEIGHT + DOCK_RADIUS, DOCK_RADIUS)
        cairo_context.fill()

