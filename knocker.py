#!/usr/bin/env python

import requests

class Knocker:

    def knock(self, targetURL):
        try:
            return requests.get(targetURL)
        except requests.exceptions.ConnectionError:
            pass

class SubDomainDiscoverer(Knocker):

    def __init__(self, domain, filePath="subdomain.list"):
        self.filePath = filePath
        self.domain = domain

    def discover(self, verbose=True):
        try:
            file = open("wordlists/"+self.filePath, "r")
            subDomainList = []

            for line in file:
                subDomainUrl = line.strip() + "." + self.domain
                response = self.knock(subDomainUrl)
                if response:
                    subDomainList.append(subDomainUrl)
                    if verbose:
                        print("[+] Subdomain Found: " + subDomainUrl)

            return subDomainList
        except Exception as e:
            print(e)
            return None

class PathFinder(Knocker):

    def __init__(self, baseURL, filepath="path.list"):
        self.filePath = filepath
        self.baseURL = baseURL

    def find(self, verbose=True):
        try:
            file = open("wordlists/"+self.filePath,"r")
            pathList = []

            for line in file:
                pathURL = self.baseURL + "/" + line.strip()
                response = self.knock(pathURL)
                if response:
                    pathList.append(pathURL)
                    if verbose:
                        print("[+] Path found: " + pathURL)

            return pathList
        except Exception as e:
            print(e)
            return None
