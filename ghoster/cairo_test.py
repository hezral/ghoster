#!/usr/bin/env python
"""Based on cairo-demo/X11/cairo-demo.c"""

import cairo
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Granite




def draw(drawing_area, cairo_context, grid):
    print(locals())
    DOCK_WIDTH = 120
    DOCK_HEIGHT = 10
    DOCK_RADIUS = 5

    PANEL_HEIGHT = 8
    PLUS_SIZE = 70
    PLUS_WIDTH = 10

    OVERLAY_COLOR = Gdk.RGBA(red=61 / 255.0, green=75 / 255.0, blue=122 / 255.0, alpha=1.0)
    height = drawing_area.get_allocated_height()
    width = drawing_area.get_allocated_width()
    gheight = grid.get_allocated_height()
    gwidth = grid.get_allocated_width()

    # height = 240
    # width = 100

    print("drawing_area: ", width, height)
    print("grid: ", width, height)

    # window
    Granite.DrawingUtilities.cairo_rounded_rectangle(cairo_context, 0, 0, width, height, 5)
    cairo_context.clip()
    cairo_context.set_line_width(4)
    Granite.DrawingUtilities.cairo_rounded_rectangle(cairo_context, 0, 0, width, height, 5)
    cairo_context.stroke()

    # wingpanel
    cairo_context.rectangle (0, 0, width, PANEL_HEIGHT)
    cairo_context.fill ()

    # plank
    Granite.DrawingUtilities.cairo_rounded_rectangle(cairo_context, (width - DOCK_WIDTH) / 2, height - DOCK_HEIGHT, DOCK_WIDTH, DOCK_HEIGHT + DOCK_RADIUS, DOCK_RADIUS)

    cairo_context.fill ();


def main():
    win = Gtk.Window()
    win.connect('destroy', Gtk.main_quit)
    win.set_default_size(450, 550)

    drawing_area = Gtk.DrawingArea()
    drawing_area.props.expand = True
    drawing_area.props.halign = Gtk.Align.FILL
    drawing_area.props.valign = Gtk.Align.FILL
    drawing_area.props.margin = 25
    drawing_area.set_size_request(300, 200)

    grid = Gtk.Grid()
    grid.attach(drawing_area, 0, 1, 1, 1)
    
    # grid.props.halign = Gtk.Align.CENTER
    # grid.props.valign = Gtk.Align.CENTER


    win.add(grid)
    drawing_area.connect('draw', draw, grid)

    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()