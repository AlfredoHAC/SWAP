#!/usr/bin/env python3

from knocker import Knocker

class Sting:

    def __init__(self, url, user="", passwd=""):
        self.XSSPoison = "<SCript>alert(\"XSS\")</scriPT>"
        self.knocker = Knocker(url, user=user, passwd=passwd)

    def injectXSS(self,form):
        data = {}
        for input in form[3]:
            data[input] = self.XSSPoison
        data[form[4]] = "submit"
        # print(form[1])
        # print(data)
        # print(form[2].lower())
        # print(form[4])
        
        response = self.knocker.knock(form[1],data,form[2].lower())
        # print(str(response.content))

        return self.XSSPoison in str(response.content)

        
