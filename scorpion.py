#!/usr/bin/env python3

from bs4 import BeautifulSoup
from claw import Claw
from sting import Sting
from urllib.parse import urljoin
import re

class Scorpion:

    def __init__(self, url, user="", passwd=""):
        self.url = url

        # GROUP (0) - FULL URL
        # GROUP (1) - PROTOCOL
        # GROUP (2) - DOMAIN/IP
        # GROUP (3) - PORT
        # GROUP (4) - PATH
        # GROUP (5) - FILE/PAGE
        # GROUP (6) - QUERY
        stripURL = re.match(r"([a-z0-9]+://)([a-z0-9]+\.[a-z0-9]+\.[a-z0-9]+\.?[0-9]*):?([0-9]*)(/?.*/)?(.*\?)?(.*)?", url)
        self.domain = stripURL.group(1) + stripURL.group(2)
        self.path = self.domain + stripURL.group(4)

        self.claw = Claw(self.url, user, passwd)
        self.sting = Sting(self.url, user, passwd)

        self.__linkList = []
        self.__formList = []
        self.vulnForms  = []
        self.vulnsFound = 0

    def extractLinks(self, url=None):
        if not url:
            url = self.url

        links = self.claw.grab("a", url)
        for link in links:
            href = link.get("href")
            href = urljoin(url, href)

            if "logout" in href:
                continue

            if "#" in href:
                href = href.split("#")[0]

            if self.domain in href and href not in self.__linkList:
                self.__linkList.append(href)
                # print("[+] Link Found: " + href)
                self.extractForms(href)
                self.extractLinks(href)
                
        return self.__linkList

    def extractForms(self, url=None):
        if not url:
            url = self.url

        forms = self.claw.grab("form", url)
        for form in forms:
            formAction = urljoin(url, form.get("action"))
            formMethod = form.get("method") if form.get("method") else "get"
            filteredInput = []
            submitName = ""

            inputList = form.findAll("input") + form.findAll("textarea")

            for input in inputList:
                if input.get("type") != "submit":
                    filteredInput.append(input.get("name"))
                else:
                    submitName = input.get("name")

            formTuple = (url, formAction, formMethod,filteredInput,submitName)
            self.__formList.append(formTuple)

        return self.__formList

    def inject(self):
        
        # print()
        for form in self.__formList:
            xssVulns = self.sting.injectXSS(form)
            
            if xssVulns:
                self.vulnsFound += 1
                self.vulnForms.append(("XSS", form[0]))
                # print("[!] XSS Vulnerability found on page " + form[0])
    
    def createLog(self):
        
        linksFoundList = '<tr><th class="tabHeader">Links Encontrados</th><td class="tabContent">'+self.__linkList[0]+'</td></tr>'
        for i in range(2, len(self.__linkList)):
            linksFoundList += '<tr><th></th><td class="tabContent">'+self.__linkList[i]+'</td></tr>'

        formsExtractedList = '<tr><th class="tabHeader">Formulários Extraídos</th><td class="tabContent">'+self.__formList[0][0]+'</td></tr>'
        for i in range(2, len(self.__formList)):
            formsExtractedList += '<tr><th></th><td class="tabContent">'+self.__formList[i][0]+'</td></tr>'

        vulnsFoundList =''
        for vuln in self.vulnForms:
            vulnsFoundList += '<tr><td class="tabContent">'+vuln[0]+'</td><td class="tabContent">'+vuln[1]+'</td></tr>'

        vulnTableList = ""
        if "XSS" in [vulnForm[0] for vulnForm in self.vulnForms]:
            vulnTableList += '''<table class="contentTable">
                            <tr>
                                <th class="tabHeader medium">Vulnerabilidade</th>
                                <td class="tabContent">Cross-Site Scripting (XSS)</td>
                            </tr>
                            <tr>
                                <th class="tabHeader medium">Descrição</th>
                                <td class="tabContent">
                                Ataques Cross-Site Scripting (XSS) ocorre quando um atacante injeta códigos maliciosos nas páginas de um site vulnerável a esse tipo de ataque,
                                sendo executado apenas no Client-Side é possível enviar a página infectada para usuários comuns a fim de cometer fraudes.
                                </td>
                            </tr>
                            <tr>
                                <th class="tabHeader medium">Nível de ameaça</th>
                                <td class="tabContent">Médio</td>
                            </tr>
                            <tr>
                                <th class="tabHeader medium">Solução</th>
                                <td class="tabContent">
                                O(s) desenvolvedor(es) do sistema deve filtrar bem as entradas do sistema, de preferência, utilizar frameworks que já
                                façam esse tipo de filtro.
                                </td>
                            </tr>
                        </table>'''


        htmlCode = """
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <link rel="stylesheet" type="text/css" href="style.css">
            <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,600,700">
            <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=PT+Sans:400,700">
            <title>SWAP - Log</title>
        </head>
        <body>
            <header>
                <h1>Resultados do Scan - SWAP</h1>
                <hr>
            </header>

            <main>
                <section id="summary">
                    <div class="divHeader">
                        <h2>Sumário</h2>
                        <h3>&#43;</h3>
                        <h3 class="hide">&#8722;</h3>
                    </div>
                    <div class="divContent">
                        <table id="summTable" class="contentTable">
                            <tr>
                                <th class="tabHeader">Domínio</th>
                                <td class="tabContent">"""+self.path+"""</td>
                            </tr>
                            <tr>
                                <th class="tabHeader">Quantidade de Vulnerabilidades Encontradas</th>
                                <td class="tabContent">"""+str(self.vulnsFound)+"""</td>
                            </tr>   
                        </table>
                    </div>
                </section>
                <section id="links">
                    <div class="divHeader">
                        <h2>Links Encontrados</h2>
                        <h3>&#43;</h3>
                        <h3 class="hide">&#8722;</h3>
                    </div>
                    <div class="divContent">
                        <table class="contentTable">
                            """+linksFoundList+"""
                        </table>
                    </div>
                </section>
                <section id="forms">
                    <div class="divHeader">
                        <h2>Formulários Extraídos</h2>
                        <h3>&#43;</h3>
                        <h3 class="hide">&#8722;</h3>
                    </div>
                    <div class="divContent">
                        <table class="contentTable">
                            """+formsExtractedList+"""
                        </table>
                    </div>
                </section>
                <section id="vulns">
                    <div class="divHeader">
                        <h2>Vulnerabilidades Detectadas</h2>
                        <h3>&#43;</h3>
                        <h3 class="hide">&#8722;</h3>
                    </div>
                    <div class="divContent">
                        <table class="contentTable">
                            <tr>
                                <th class="tabHeader">Vulnerabilidade</th>
                                <th class="tabHeader">Formulário</th>
                            </tr>"""+vulnsFoundList+"""
                        </table>
                    </div>
                </section>
                <section id="advanced">
                    <div class="divHeader">
                        <h2>Avançado</h2>
                        <h3>&#43;</h3>
                        <h3 class="hide">&#8722;</h3>
                    </div>
                    <div class="divContent">"""+vulnTableList+"""</div>
                </section>
            </main>
            
            <script>

                var headers = document.getElementsByClassName("divHeader");
                var i;

                for (i = 0; i < headers.length; i++) {
                        headers[i].addEventListener("click", function () {
                            this.classList.toggle("active");
                            var content = this.nextElementSibling;
                            if (content.style.maxHeight) {
                                this.children[1].className = ""
                                this.children[2].className = "hide" 
                                content.style.maxHeight = null;
                            } else {
                                this.children[1].className = "hide"
                                this.children[2].className = "" 
                                content.style.maxHeight = content.scrollHeight + "px";
                            }
                            
                        });
                    }

            </script>
        </body>
        </html>
        """

        htmlFile = open ("Log/swapLog.html", "w")
        htmlFile.write(htmlCode)
        htmlFile.close()

        