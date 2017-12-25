#! /usr/bin/python3

import website
import time

class Manage_websites:
    """class groups all the websites checked by the program"""

    def __init__(self):
        """at the beginning of the program, no websites are checked"""
        self.websites = {}

    def add_website(self,name, url, check_interval):
        """add a website to the list of websites to check."""
        self.websites[name] = website.Website(url,int(check_interval))

    def remove_website(self, name):
        """remove a website from the list of websites to check."""
        del websites[name]

    def change_url(self, name, url):
        """change the url of the website"""
        try:
            websites[name].change_url(url)
        except:
            print("The website {} doesn't exist".format(name))

    def change_chek_interval(self, name, url):
        """change the period between two checks"""
        try:
            websites[name].change_check_interval(url)
        except:
            print("The website {} doesn't exist".format(name))

    def display_websites(self):
        """Displays all the websites checked by the program"""
        for name in self.websites:
            print("{} : {}".format(name, str(self.websites[name])))

    def run_short_period(self):
        """thread that every 10s, displays the stats for each website for the last 10m"""
        while True:
            for name in self.websites:
            time.sleep(10)
        pass

