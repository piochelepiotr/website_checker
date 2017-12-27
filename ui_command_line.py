#! /usr/bin/python3

import urwid
from manage_websites import Manage_websites
from prints import print_info


class CommandLine(urwid.Edit):

    def __init__(self, websites):
        self.websites = websites
        self.build_commands()
        super().__init__(("command", "> "))

    def build_commands(self):
        self.commands = {}
        self.commands["help"] = CommandLine.help
        self.commands["add"] = Manage_websites.add_website
        self.commands["remove"] = Manage_websites.remove_website
        self.commands["change_url"] = Manage_websites.change_url
        self.commands["change_check_interval"] = Manage_websites.change_check_interval
        self.commands["display"] = Manage_websites.display_websites

    def keypress(self, size, key):
        if key != "enter":
            return super().keypress(size, key)
        self.execute_command(self.edit_text)
        self.edit_text = ""

    def help(self):
        """all the available commands and how to use them
        use : help"""
        print_info("Available commands :")
        for command in self.commands:
            print_info("- {} : {}".format(command, self.commands[command].__doc__))

    def execute_command(self, command):
        L = command.split(" ")
        if len(L) == 0 or L[0] == "help":
            self.help()
        elif L[0] == "exit":
            exit()
        elif L[0] in self.commands:
            try:
                self.commands[L[0]](self.websites, *L[1:])
            except KeyError:
                print_info("Invalid use of command")
        else:
            print_info("Command does not exist")

