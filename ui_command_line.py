#! /usr/bin/python3

import urwid
from manage_websites import Manage_websites
from prints import print_command


class CommandLine(urwid.Edit):
    """this class is the edit line where
    the user can enter a command"""

    def __init__(self, websites):
        """inits the command line"""
        self.websites = websites
        self.build_commands()
        super().__init__(("command", "> "))

    def build_commands(self):
        """adds all the commands to a dictionary,
        so that they can be used by the user later"""
        self.commands = {}
        self.commands["help"] = CommandLine.help
        self.commands["add"] = Manage_websites.add_website
        self.commands["remove"] = Manage_websites.remove_website
        self.commands["change_url"] = Manage_websites.change_url
        self.commands["change_check_interval"] = Manage_websites.change_check_interval
        self.commands["display"] = Manage_websites.display_websites

    def keypress(self, size, key):
        """if the key pressed is enter,
        execute the command"""
        if key != "enter":
            return super().keypress(size, key)
        self.execute_command(self.edit_text)
        self.edit_text = ""

    def help(self):
        """all the available commands and how to use them
        use : help"""
        print_command("Available commands :")
        for command in self.commands:
            print_command("- {} : {}".format(command, self.commands[command].__doc__))

    def execute_command(self, command):
        """execute the command if it is
        a correct command"""
        L = command.split(" ")
        if len(L) == 0 or L[0] == "help":
            self.help()
        elif L[0] in self.commands:
            try:
                self.commands[L[0]](self.websites, *L[1:])
            except TypeError:
                print_command("Invalid use of command")
        else:
            print_command("Command {} does not exist".format(L[0]))

