#! /usr/bin/python3

import urwid

class TextZone(urwid.Frame):
    def keypress(self, size, key):
        self.add_text("truc")

    def __init__(self, title, style = "default"):
        self.style = style
        self.walker = urwid.SimpleListWalker([])
        self.txt_zone = urwid.ListBox(self.walker)
        self.add_text("hey")
        self.title = urwid.Text(("title", title))
        super().__init__(self.txt_zone, header=self.title)

    def add_text(self, txt):
        self.walker.append(urwid.Text((self.style, txt)))

