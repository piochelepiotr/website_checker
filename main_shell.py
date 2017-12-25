#! /usr/bin/python3

import cmd
import manage_websites

websites = manage_websites.Manage_websites()

class MainShell(cmd.Cmd):
    """a shell with all the commands used for this project"""
    intro = "Welcome to the main shell, Type help or ? to list commands.\n"
    prompt = ">>>"
    file = None
    def do_add(self, arg):
        """add a website to the list of websites to check.
        use : add name url check_interval"""
        try:
            manage_websites.Manage_websites.add_website(websites, *arg.split())
        except Exception as e:
            print("Wrong use of command")
            print(e)

    def do_remove(self, arg):
        """remove a website from the list of websites to check.
        use : remove name"""
        try:
            manage_websites.Manage_websites.remove_website(websites, *arg.split())
        except Exception as e:
            print("Wrong use of command")
            print(e)

    def do_change_url(self, arg):
        """change the url of the website
        use : change_url name new_url"""
        try:
            manage_websites.Manage_websites.change_url(websites, *arg.split())
        except Exception as e:
            print("Wrong use of command")
            print(e)

    def do_change_check_interval(self, arg):
        """change the period between two checks
        use : change_check_interval name new_check_interval"""
        try:
            manage_websites.Manage_websites.change_check_interval(websites, *arg.split())
        except Exception as e:
            print("Wrong use of command")
            print(e)

    def do_display(self, arg):
        """Displays all the websites checked by the program
        use : display"""
        try:
            manage_websites.Manage_websites.display_websites(websites, *arg.split())
        except Exception as e:
            print("Wrong use of command")
            print(e)
    def do_exit(self, arg):
        """Exits the program
        use : exit"""
        exit()

if __name__ == "__main__":
    MainShell().cmdloop()
