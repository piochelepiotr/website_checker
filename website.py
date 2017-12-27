#! /usr/bin/python3

import threading
import requests
import time
import response
import bisect
from prints import print_info
from prints import print_alert


def group_list(L):
    """groups elements of a list in a dictionary :
    the key is the element,
    the value is the number of occurencies of the element in the list"""
    d = {}
    for x in L:
        try:
            d[x] += 1
        except KeyError:
            d[x] = 1
    return d


def print_website_stats(
        name, availability, error_codes, avg_resp_time,
        min_resp_time, max_resp_time):
    txt = """{}
availability of {}%
response time (avg, min, max) : {}s {}s {}s
error codes : {}""".format(
        name, availability, avg_resp_time, min_resp_time,
        max_resp_time, error_codes)
    print_info(txt)


class Website:
    """class Website regulary checks wether a website is down or not,
    it can then provide information on a website availability and
    response time"""

    def __init__(self, name, url, check_interval, ok_responses):
        """inits a website checker with an url and
        a check_interval : time between two checks"""
        self.url = url
        self.name = name
        self.check_interval = check_interval
        self.ok_responses = ok_responses
        self.responses = []
        self.wrong_url = False
        self.available = True
        self.lock = threading.Lock()
        self.thread_check = threading.Thread(
                target=Website.run_check, args=(self,))
        self.thread_check.daemon = True
        self.thread_check.start()
        if not self.check():
            print_info("Impossible to reach Website, check the URL and your internet connection")

    def change_url(self, url):
        """change the url of the website"""
        self.wrong_url = False
        self.url = url
        self.responses = []
        self.available = True
        if not self.check():
            print_info("Impossible to reach Website, check the URL and your internet connection")

    def change_check_interval(self, check_interval):
        """change the time between two checks"""
        if check_interval <= 0:
            print_info("Minimum check interval = 1s")
            check_interval = 1
        self.check_interval = check_interval

    def check(self):
        """checks the website, if there is an error, the url is wrong or
        the internet connection is down"""
        try:
            r = requests.get(self.url)
        except requests.exceptions.MissingSchema:
            # url not valid
            self.responses.append(response.Response(-1, -1, time.time()))
            self.wrong_url = True
            return False
        except requests.exceptions.ConnectionError:
            # maybe no internet, maybe wrong url but we consider that the website is down
            self.responses.append(response.Response(-1, -1, time.time()))
            return False
        self.responses.append(response.Response(
            int(r.status_code), r.elapsed.total_seconds(),
            time.time()))
        return int(r.status_code) in self.ok_responses

    def check_available(self):
        availability, err, avg, m, M = self.get_stats(60*2)
        if availability > 80 and  not self.available:
            print_alert("Website {} is once again available".format(self.name))
            self.available = True
        elif availability < 80 and self.available:
            print_alert("Website {} is no longer available".format(self.name))
            self.available = False

    def run_check(self):
        """thread that checks regulary if the website is down or not"""
        while True:
            self.lock.acquire()
            if not self.wrong_url:
                self.check()
            self.lock.release()
            self.check_available()
            time.sleep(self.check_interval)

    def remove_old_request(self):
        """in order to free space, removes unused data"""
        pass

    def get_stats(self, period):
        """prints some stats on a website availability and response time"""
        self.lock.acquire()
        start_index = bisect.bisect_left(self.responses, time.time() - period)
        responses = self.responses[start_index:]
        if len(responses) == 0:
            return (0, {}, 0, 0, 0)
        resp_codes = [response.response_code for response in self.responses]
        error_codes = group_list(resp_codes)
        sum_ok = sum([error_codes[code] for code in self.ok_responses if code in error_codes])
        availability = sum_ok / sum(error_codes.values()) * 100
        resp_times = [response.response_time for response in responses if response.response_time != -1]
        avg_resp_time = 0
        min_resp_time = 0
        max_resp_time = 0
        if len(resp_times) > 0:
            avg_resp_time = sum(resp_times)/len(resp_times)
            min_resp_time = min(resp_times)
            max_resp_time = max(resp_times)
        self.lock.release()
        return (availability, error_codes,
                avg_resp_time, min_resp_time, max_resp_time)

    def __repr__(self):
        """return an str representing the website"""
        return "{} : {}, check : {}s, status : {}".format(
                self.name,
                self.url,
                self.check_interval,
                "available" if self.available else "not available")
