#! /usr/bin/python3

import website
import time
import threading


class Manage_websites:
    """class groups all the websites checked by the program"""

    config_file = "config.txt"

    def __init__(self):
        """at the beginning of the program, no websites are checked"""
        self.websites = {}
        self.load_config()
        self.thread_short_period = threading.Thread(
                target=Manage_websites.disp_short_period, args=(self,))
        self.thread_short_period.daemon = True
        self.thread_short_period.start()

    def add_website(self, name, url, check_interval):
        """add a website to the list of websites to check."""
        if name in self.websites:
            print("Website {} already exists.".format(name))
        else:
            self.websites[name] = website.Website(
                    url, int(check_interval), self.config)

    def remove_website(self, name):
        """remove a website from the list of websites to check."""
        if name in self.websites:
            del self.websites[name]
        else:
            print("Website {} doesn't exist.".format(name))

    def change_url(self, name, url):
        """change the url of the website"""
        try:
            self.websites[name].change_url(url)
        except KeyError:
            print("The website {} doesn't exist".format(name))

    def change_chek_interval(self, name, url):
        """change the period between two checks"""
        try:
            self.websites[name].change_check_interval(url)
        except KeyError:
            print("The website {} doesn't exist".format(name))

    def display_websites(self):
        """Displays all the websites checked by the program"""
        for name in self.websites:
            print("{} : {}".format(name, str(self.websites[name])))

    def disp_short_period(self):
        """thread that every 10s,
        displays the stats for each website for the last 10m"""
        while True:
            for name in self.websites:
                pass
            time.sleep(10)

    def load_config(self):
        """loads the configuration file that indicates in what case
        a website is considered down
        by default, only 200 response code means the website is ok"""
        self.config = [200]
        try:
            with open(self.config_file, "r") as f:
                f.readline()
                self.config = [int(x) for x in f.readline().split(",")]
        except FileNotFoundError:
            print("Configuration file not found, using default configuration")
        except ValueError:
            print("Configuration file incorrect, using default configuration")
