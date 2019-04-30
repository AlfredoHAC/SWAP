#!/usr/bin/env python3

import requests as Requests

class Knocker:

    def __init__(self, url, user="", passwd=""):
        self.session = Requests
        self.url = url
        
        if user and passwd:
            self.session = Requests.Session()
            self.session.post(self.url,{"username":"admin","password":"password", "Login":"Login"})
        
    def knock(self, targetURL=None, data={}, method="get"):
        if not targetURL:
            targetURL = self.url

        try:
            if method.lower() == "post":
                return self.session.post(targetURL, data=data)

            return self.session.get(targetURL, params=data)
        except Requests.exceptions.ConnectionError:
            pass

