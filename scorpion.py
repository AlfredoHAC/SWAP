#!/usr/bin/env python

from bs4 import BeautifulSoup
from knocker import Knocker
from urllib.parse import urljoin
import re

class Scorpion:

    def __init__(self, url):
        self.knocker = Knocker()
        self.url = url

        stripURL = re.match(r"([a-z0-9]+://)([a-z0-9]+\.[a-z0-9]+\.[a-z0-9]+\.?[0-9]*):?([0-9]*)(/?.*/)?(.*\?)?(.*)?", url)
        self.domain = stripURL.group(1) + stripURL.group(2)
        self.path = self.domain + stripURL.group(4)

        self.__linkList = []
        self.__formList = []

    def crawl(self, htmlElement, url=None):
        if url == None:
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

    def extractLinks(self, url=None):
        if url == None:
            url = self.url

        links = self.crawl("a", url)
        for link in links:
            href = link.get("href")
            href = urljoin(url, href)

            if "#" in href:
                href = href.split("#")[0]

            if self.domain in href and href not in self.__linkList:
                self.__linkList.append(href)
                print("[+] Link Found: " + href)
                self.extractForms(href)
                self.extractLinks(href)
                
        return self.__linkList

    def extractForms(self, url=None):
        if url == None:
            url = self.url

        forms = self.crawl("form", url)
        for form in forms:
            formAction = urljoin(url, form.get("action"))
            formMethod = form.get("method") if form.get("method") else "get"

            formTuple = ((url, formAction, formMethod,[]))
            inputList = form.findAll("input") + form.findAll("textarea") + form.findAll("select")

            # print(inputList)
            for input in inputList:
                if input.get("type") != "submit":
                    formTuple[3].append(input.get("name"))
            self.__formList.append(formTuple)

        return self.__formList
