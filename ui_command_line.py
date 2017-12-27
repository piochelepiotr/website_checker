#! /usr/bin/python3

import urwid

class Command(urwid.Edit):

    def __init__(self):
        super().__init__(("command", "> "))

    def keypress(self, size, key):
        if key != "enter":
            return super().keypress(size, key)
        self.edit_text = ""
