#! /usr/bin/python3

import threading
import requests
import time
import response
import bisect


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
    print("Website {} has ".format())


class Website:
    """class Website regulary checks wether a website is down or not,
    it can then provide information on a website availability and
    response time"""

    def __init__(self, url, check_interval):
        """inits a website checker with an url and
        a check_interval : time between two checks"""
        self.url = url
        self.check_interval = check_interval
        self.responses = []
        self.valid_website = True
        self.lock = threading.Lock()
        self.thread_check = threading.Thread(
                target=Website.run_check, args=(self,))
        self.thread_check.daemon = True
        self.thread_check.start()

    def change_url(self, url):
        """change the url of the website"""
        self.valid_website = True
        self.url = url

    def change_check_interval(self, check_interval):
        """change the time between two checks"""
        self.check_interval = check_interval

    def check(self):
        """checks the website, if there is an error, the url is wrong or
        the internet connection is down"""
        try:
            r = requests.get(self.url)
        except requests.exceptions.MissingSchema:
            print("URL {} is invalid, you need to change it.".format(self.url))
            self.valid_website = False
            return
        self.responses.append(response.Response(
            r.elapsed.total_seconds(),
            int(r.status_code), time.time()))

    def run_check(self):
        """thread that checks regulary if the website is down or not"""
        while True:
            self.lock.acquire()
            if self.valid_website:
                self.check()
            self.lock.release()
            time.sleep(self.check_interval)

    def remove_old_request(self):
        """in order to free space, removes unused data"""
        pass

    def get_stats(self, period):
        """prints some stats on a website availability and response time"""
        self.lock.acquire()
        start_index = bisect.bisect_left(self.responses, time.time() - period)
        responses = self.responses[start_index:]
        resp_codes = [response.reponse_code for response in self.responses]
        error_codes = group_list(resp_codes)
        availability = error_codes[200] / sum(error_codes.values) * 100
        resp_times = [response.respnse_time for response in responses]
        avg_resp_time = sum(resp_times)/len(resp_times)
        min_resp_time = min(resp_times)
        max_resp_time = max(resp_times)
        self.lock.release()
        return (availability, error_codes,
                avg_resp_time, min_resp_time, max_resp_time)

    def __repr__(self):
        """return an str representing the website"""
        return "{} , check : {}, status : {}".format(
                self.url,
                self.check_interval,
                "ok" if self.valid_website else "invalid url")
