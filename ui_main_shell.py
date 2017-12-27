#! /usr/bin/python3

import urwid
from ui_command_line import CommandLine
import prints
import manage_websites

class MainShell(urwid.Frame):
    def __init__(self):
        self.websites = manage_websites.Manage_websites()
        self.infos = prints.infos
        self.alerts = prints.alerts
        self.layout = urwid.Columns([self.alerts, self.infos])
        self.command = CommandLine(self.websites)
        super().__init__(self.layout, footer=self.command, focus_part="footer")

if __name__ == "__main__":
    palette = [
            ('command', 'default,bold', 'default', 'bold'),
            ('alert', 'dark red', 'default'),
            ('title','black','dark cyan', 'standout')
            ]

    main_shell = MainShell()
    urwid.MainLoop(main_shell, palette).run()
