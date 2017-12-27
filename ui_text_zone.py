#! /usr/bin/python3

import urwid

class TextZone(urwid.Frame):
    """this class is an output text class
    it is composed of a title and a scrollable
    content"""

    __metaclass__ = urwid.MetaSignals
    signals = ["content_changed"]

    def __init__(self, title, style = "default"):
        """inits the Text zone with the title and
        the content"""
        self.style = style
        self.walker = urwid.SimpleListWalker([])
        self.txt_zone = urwid.ListBox(self.walker)
        self.title = urwid.Text(("title", title))
        super().__init__(self.txt_zone, header=self.title)

    def add_text(self, txt):
        """add text to content, set focus on the last
        element to make autoscroll work"""
        self.walker.append(urwid.Text((self.style, txt)))
        #print(self.walker.focus)
        self.txt_zone.set_focus(len(self.walker)-1)
        urwid.emit_signal(self, "content_changed")

