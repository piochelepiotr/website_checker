#! /usr/bin/python3

import urwid
from ui_command_line import CommandLine
import prints
import manage_websites


class MainShell(urwid.Frame):
    """this class is the main window composed of :
    3 subwindows : command output, alerts and informations
    one command line input"""
    def __init__(self):
        """create all the elements and calls the super init to finish
        the construction of the frame"""
        self.websites = manage_websites.Manage_websites()
        self.infos = prints.infos
        self.alerts = prints.alerts
        self.command_out = prints.command_out
        self.layout = urwid.Columns(
                [self.command_out, self.alerts, self.infos])
        self.command = CommandLine(self.websites)
        super().__init__(self.layout, footer=self.command, focus_part="footer")


class MainLoop(urwid.MainLoop):
    """this class is used to display
    the main window"""

    def __init__(self):
        """create all the elements and connects
        the signals to enable refresh"""
        self.palette = [
                ('command', 'default,bold', 'default', 'bold'),
                ('alert', 'dark red', 'default'),
                ('title', 'black', 'dark cyan', 'standout')
                ]
        self.main_shell = MainShell()
        super().__init__(self.main_shell, self.palette)
        urwid.connect_signal(self.main_shell.command_out, "content_changed", MainLoop.draw_screen, user_args=[self])
        urwid.connect_signal(self.main_shell.infos, "content_changed", MainLoop.draw_screen, user_args=[self])
        urwid.connect_signal(self.main_shell.alerts, "content_changed", MainLoop.draw_screen, user_args=[self])
