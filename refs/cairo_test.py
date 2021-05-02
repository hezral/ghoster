#!/usr/bin/env python
"""Based on cairo-demo/X11/cairo-demo.c"""

import cairo
import gi
gi.require_version("Gtk", "3.0")
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gdk, Granite




class AppContainer(Gtk.Button):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.props.name = name
        
        #self.props.label = name
        self.props.image = Gtk.Image().new_from_icon_name("com.github.hezral.inspektor", Gtk.IconSize.LARGE_TOOLBAR)
        self.props.always_show_image = True
        self.props.expand = False
        self.props.halign = self.props.valign = Gtk.Align.CENTER
        self.props.margin = 2
        #self.set_size_request(50, 10)

        self.connect("realize", self.on_realize)

    def on_realize(self, *args):
        print(locals())
        layout = self.get_parent()
        print(layout.get_allocation().x)
        print(layout.get_allocation().y)
        layout.move(self, 50, 50)



class WorkspaceArea(Gtk.DrawingArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.props.expand = True
        self.props.halign = self.props.valign = Gtk.Align.FILL
        self.props.margin = 25
        self.set_size_request(300, 200)
        self.connect("draw", self.draw)

    def draw(self, drawing_area, cairo_context):
        #print(locals())
        DOCK_WIDTH = 120
        DOCK_HEIGHT = 10
        DOCK_RADIUS = 3

        PANEL_HEIGHT = 8
        PLUS_SIZE = 70
        PLUS_WIDTH = 10

        OVERLAY_COLOR = Gdk.RGBA(red=61 / 255.0, green=75 / 255.0, blue=122 / 255.0, alpha=1.0)
        height = drawing_area.get_allocated_height()
        width = drawing_area.get_allocated_width()


        # height = 200
        # width = 300

        #print("drawing_area: ", width, height)



        #cairo_context.set_source_rgba(OVERLAY_COLOR.red, OVERLAY_COLOR.green, OVERLAY_COLOR.blue, OVERLAY_COLOR.alpha)

        # window
        Granite.DrawingUtilities.cairo_rounded_rectangle(cairo_context, 0, 0, width, height, 4)
        cairo_context.clip()
        cairo_context.set_line_width(4)
        Granite.DrawingUtilities.cairo_rounded_rectangle(cairo_context, 0, 0, width, height, 4)
        cairo_context.stroke()

        # wingpanel
        cairo_context.rectangle (0, 0, width, PANEL_HEIGHT)
        cairo_context.fill()

        # plank
        Granite.DrawingUtilities.cairo_rounded_rectangle(cairo_context, (width - DOCK_WIDTH) / 2, height - DOCK_HEIGHT, DOCK_WIDTH, DOCK_HEIGHT + DOCK_RADIUS, DOCK_RADIUS)
        cairo_context.fill()

def main():
    win = Gtk.Window()
    
    win.connect('destroy', Gtk.main_quit)

    app1 = AppContainer("app1")
    #app2 = AppContainer("app2")

    layout = Gtk.Layout()
    layout.set_size_request(300, 200)
    layout.props.expand = True
    layout.props.halign = layout.props.valign = Gtk.Align.FILL
    layout.props.margin = 25
    layout.add(app1)
    layout.move(app1, 10, 10)

    d1 = WorkspaceArea()



    overlay = Gtk.Overlay()
    
    overlay.add(d1)
    #overlay.add_overlay(app1)
    #overlay.add_overlay(app2)

    grid = Gtk.Grid()
    grid.attach(layout, 0, 1, 1, 1)
    grid.attach(overlay, 0, 1, 1, 1)
    grid.props.halign = grid.props.valign = Gtk.Align.CENTER
    
    win.add(grid)


    

    win.show_all()


    


if __name__ == '__main__':
    main()
    Gtk.main()