#! /usr/bin/python3

import threading

def foo():
    threading.Timer(0.000000000001,foo).start()

threading.Timer(0,foo).start()
