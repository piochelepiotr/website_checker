#! /usr/bin/python3

import requests
import threading
import bisect
import time
import cmd

def group_list(L):
    d = {}
    for x in L:
        try:
            d[x] += 1
        except:
            d[x] = 1
    return d

class Response:

    def __init__(self, response_code, response_time, create_time):
        self.response_code = response_code
        self.response_time = response_time
        self.create_time = create_time

    def is_old(self, current_time, old_period):
        return self.create_time + old_period > current_time

    def __gt__(self, other):
        return self.create_time > other.create_time

class Website:

    def __init__(self, url, check_interval):
        self.url = url
        self.check_interval = check_interval
        self.responses = []
        self.valid_website = True
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=Website.run,args=(self,))
        self.thread.start()

    def change_url(self, url):
        self.valid_website = True
        self.url = url

    def change_check_interval(self, check_interval):
        self.check_interval = check_interval

    def check(self):
        try:
            r = requests.get(self.url)
            self.responses.append(Response(r.elapsed.total_seconds(), int(r.status_code),time.time()))
        except:
            print("URL {} is invalid, you need to change it.".format(self.url))
            self.valid_website = False

    def run(self):
        while True:
            self.lock.acquire()
            if self.valid_website:
                self.check()
            self.lock.release()
            time.sleep(self.check_interval)

    def remove_old_request(self):
        pass

    def get_stats(self,period):
        self.lock.acquire()
        start_index = bisect.bisect_left(responses, time.time() - period)
        responses = self.responses[start_index:]
        error_codes = group_list([reponse.reponse_code for response in responses])
        availability = error_codes[200] / sum(error_codes.values) * 100
        resp_times = [response.respnse_time for response in responses]
        avg_resp_time = sum(resp_times)/len(resp_times)
        min_resp_time = min(resp_times)
        max_resp_time = max(resp_times)
        self.lock.release()

class Manage_websites:
    def __init__(self):
        self.websites = {}

    def add_website(self,name, url, check_interval):
        """add a website to the list of websites to check.
        use : add name url check_interval"""
        self.websites[name] = Website(url,int(check_interval))

    def remove_website(self, name):
        """remove a website from the list of websites to check.
        use : remove name"""
        del websites[name]

    def change_url(self, name, url):
        """change the url of the website
        use : change_url name new_url"""
        try:
            websites[name].change_url(url)
        except:
            print("The website {} doesn't exist".format(name))

    def change_chek_interval(self, name, url):
        """change the period between two checks
        use : change_check_interval name new_check_interval"""
        try:
            websites[name].change_check_interval(url)
        except:
            print("The website {} doesn't exist".format(name))

    def display_websites(self):
        """Displays all the websites checked by the program
        use : display"""

def help(commands):
    """Prints all the commands and how to use them"""
    print("Available commands :")
    for name in commands:
        print("- {} : {}".format(name,commands[name].__doc__))

def exit_program():
    """Exits the program"""
    exit()

commands = {}
commands["help"] = help
commands["add"] = Manage_websites.add_website
commands["remove"] = Manage_websites.remove_website
commands["change_url"] = Manage_websites.change_url
commands["change_check_interval"] = Manage_websites.change_chek_interval
commands["display"] = Manage_websites.display_websites
commands["exit"] = exit_program
websites = Manage_websites()

class MainShell(cmd.Cmd):
    intro = "Welcome to the main shell, Type help or ? to list commands.\n"
    prompt = ">>>"
    file = None
    def do_add(self, arg):
        """add a website to the list of websites to check.
        use : add name url check_interval"""
        try:
            Manage_websites.add_website(websites,*arg.split())
        except Exception as e:
            print("Wrong use of command")
            print(e)

    def do_remove(self, arg):
        """remove a website from the list of websites to check.
        use : remove name"""
        try:
            Manage_websites.remove_website(websites,*arg.split())
        except Exception as e:
            print("Wrong use of command")
            print(e)

    def do_change_url(self, arg):
        """change the url of the website
        use : change_url name new_url"""
        try:
            Manage_websites.change_url(websites,*arg.split())
        except Exception as e:
            print("Wrong use of command")
            print(e)

    def do_change_check_interval(self, arg):
        """change the period between two checks
        use : change_check_interval name new_check_interval"""
        try:
            Manage_websites.change_check_interval(websites,*arg.split())
        except Exception as e:
            print("Wrong use of command")
            print(e)

    def do_display(self, arg):
        """Displays all the websites checked by the program
        use : display"""
        try:
            Manage_websites.display_websites(websites,*arg.split())
        except Exception as e:
            print("Wrong use of command")
            print(e)

def analyse_command(command):
    """analyse user's input and execute command given by the user"""
    words = command.split(" ")
    if(len(words) > 0 and words[0] in commands and words[0] != "help"):
        name = words[0]
        args = words[1:]
        if name == "exit":
            exit_program()
        else:
            commands[name](websites, *args)
            try:
                pass
            except:
                print("Invalid use of {}, try to use help.".format(name))
    else:
        commands["help"](commands)

def main():
    while True:
        command = input("Enter a command :\n>>>")
        analyse_command(command)
        print()

if __name__ == "__main__":
    #main()
    MainShell().cmdloop()
