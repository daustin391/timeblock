""" Views
    Handle display of text interface for Timeblock app
"""
import urwid


def menu():
    """Create top-menu widget"""
    bg = urwid.SolidFill(" ")
    menu_text = urwid.Text("(A) Add item")
    menu_box = urwid.Filler(menu_text)
    screen = urwid.Overlay(menu_box, bg, "left", ("relative", 100), "bottom", 1)
    return screen


def display(view):
    """Display widget on screen"""
    loop = urwid.MainLoop(view)
    loop.run()
