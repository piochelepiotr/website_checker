#! /usr/bin/python3


class Response:
    """this class describes a response of a website,
    it includes the response code, the response time
    and the time of the response"""

    def __init__(self, response_code, response_time, create_time):
        """inits the response"""
        self.response_code = response_code
        self.response_time = response_time
        self.create_time = create_time

    def is_old(self, current_time, old_period):
        """returns true if the response is older than old_period"""
        return self.create_time + old_period > current_time

    def __gt__(self, other):
        """implemented > operator, for bisect search"""
        if isinstance(other, Response):
            return self.create_time > other.create_time
        elif isinstance(other, float):
            return self.create_time > other

    def __lt__(self, other):
        """implemented > operator, for bisect search"""
        if isinstance(other, Response):
            return self.create_time < other.create_time
        elif isinstance(other, float):
            return self.create_time < other
