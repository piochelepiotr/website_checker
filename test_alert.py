#! /usr/bin/python3

import ui_main_shell
import threading
import time


def do_test(loop):
    """this is the test sequence :
    * adds a correct website
    * waits
    * changes the website to an incorrect one
    * waits
    * changes to a correct
    * waits"""
    time.sleep(1)
    websites = loop.main_shell.websites
    # everything is ok
    websites.add_website("google", "http://www.google.com", 1)
    time.sleep(60)
    # now, we change the adress so the requests will fail
    # the program should display an alert
    websites.websites["google"].url = "http://www.google2.com"
    time.sleep(30)
    # we put back the good adress, an other alert should be printed
    websites.websites["google"].url = "http://www.google.com"
    time.sleep(60)


if __name__ == "__main__":
    """creates the main shell and
    starts the test"""
    loop = ui_main_shell.MainLoop()
    thread = threading.Thread(target=do_test, args=(loop,))
    thread.daemon = True
    thread.start()
    loop.run()
