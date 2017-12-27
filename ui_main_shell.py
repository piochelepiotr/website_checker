#! /usr/bin/python3

import urwid
import command_line
import text_zone

palette = [
        ('command', 'default,bold', 'default', 'bold'),
        ('alert', 'dark red', 'default'),
        ('title','black','dark cyan', 'standout')
        ]

class MainWindow(urwid.Frame):
    def __init__(self):
        alerts = TextZone("Alerts", "alert")
        infos = TextZone("Informations")
        layout = urwid.Columns([alerts, infos])
        command = Command()
        super().__init__(layout, footer=command, focus_part="footer")

urwid.MainLoop(MainWindow(), palette).run()
