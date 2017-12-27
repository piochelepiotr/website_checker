#! /usr/bin/python3

from ui_text_zone import TextZone

try:
    print(infos)
except NameError:
    infos = TextZone("Informations")

try:
    print(alerts)
except NameError:
    alerts = TextZone("Alerts", "alert")

def print_info(txt):
    infos.add_text(txt)

def print_alert(txt):
    alerts.add_text(txt)
