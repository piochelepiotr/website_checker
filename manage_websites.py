#! /usr/bin/python3

import website
import time
import threading
from prints import print_info


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
        self.thread_long_period = threading.Thread(
                target=Manage_websites.disp_long_period, args=(self,))
        self.thread_long_period.daemon = True
        self.thread_short_period.start()
        self.thread_long_period.start()

    def add_website(self, name, url, check_interval):
        """add a website to the list of websites to check.
        use : add name url check_interval"""
        if name in self.websites:
            print_info("Website {} already exists.".format(name))
        else:
            self.websites[name] = website.Website(
                    name, url, int(check_interval), self.config)

    def remove_website(self, name):
        """remove a website from the list of websites to check.
        use : remove name"""
        if name in self.websites:
            del self.websites[name]
        else:
            print_info("Website {} doesn't exist.".format(name))

    def change_url(self, name, url):
        """change the url of the website
        use : change_url name new_url"""
        try:
            self.websites[name].change_url(url)
        except KeyError:
            print_info("The website {} doesn't exist".format(name))

    def change_check_interval(self, name, check_interval):
        """change the period between two checks
        use : change_check_interval name new_check_interval"""
        try:
            self.websites[name].change_check_interval(int(check_interval))
        except KeyError:
            print_info("The website {} doesn't exist".format(name))

    def display_websites(self):
        """Displays all the websites checked by the program
        use : display"""
        for name in self.websites:
            print_info(str(self.websites[name]))

    def disp_short_period(self):
        """thread that every 10s,
        displays the stats for each website for the last 10m"""
        while True:
            if len(self.websites) > 0:
                print_info("\nStatistics for the last 10m")
            for name in self.websites:
                stats = self.websites[name].get_stats(10*60)
                website.print_website_stats(name, *stats)
                #if availability is greater than 80% and status = not ok, then put the status at ok and print
                #if availability is lower than 80% and status = ok, then put the status at not ok and print
            time.sleep(2)

    def disp_long_period(self):
        """thread that every 1m,
        displays the stats for each website for the last hour"""
        while True:
            if len(self.websites) > 0:
                print_info("\nStatistics for the last hour")
            for name in self.websites:
                stats = self.websites[name].get_stats(60*60)
                website.print_website_stats(name, *stats)
            time.sleep(60)

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
            print_info("Configuration file not found, using default configuration")
        except ValueError:
            print_info("Configuration file incorrect, using default configuration")
