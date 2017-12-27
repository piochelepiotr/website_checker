#! /usr/bin/python3

import time
from ui_text_zone import TextZone

try:
    print(infos)
except NameError:
    infos = TextZone("Informations")

try:
    print(alerts)
except NameError:
    alerts = TextZone("Alerts", "alert")

try:
    print(command_out)
except NameError:
    command_out = TextZone("Command outputs")

def print_info(txt):
    """prints an str the information window"""
    infos.add_text(txt)

def print_alert(txt):
    """prints an str the alert window, adds the time at the beggining of the message"""
    alerts.add_text(str(time.ctime()) + " : " + txt)

def print_command(txt):
    """prints an str in the command window"""
    command_out.add_text(txt)
