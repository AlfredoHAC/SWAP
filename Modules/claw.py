#!/usr/bin/env python3

from bs4 import BeautifulSoup
from knocker import Knocker

class Claw:

    def __init__(self, url, user="", passwd=""):
        self.url = url
        self.knocker = Knocker(url, user, passwd)
    
    def grab(self, htmlElement, url=None):
        if not url:
            url = self.url

        response = self.knocker.knock(url)

        if not response:
            return None

        header = response.headers

        type = header.get("Content-Type")
        if "text/html" not in type:
            return []

        parsedHTML = BeautifulSoup(response.content, "lxml")
        return parsedHTML.findAll(htmlElement)