#!/usr/bin/env python

from scorpion import Scorpion

# url = "http://dhsistemas.com.br/"
# url = "https://seguro.uern.br/integra/"
# url = "https://di.uern.br/moodle/"
# url = "http://192.168.0.105/mutillidae/index.php?page=dns-lookup.php"
# url = "http://192.168.0.105/mutillidae/index.php?page=text-file-viewer.php"
# url = "http://192.168.0.105/mutillidae/index.php?page=add-to-your-blog.php"
# url = "http://192.168.0.106/mutillidae/documentation/mutillidae-installation-on-xampp-win7.pdf"
url = "http://192.168.0.105/mutillidae/"

crawler = Scorpion(url)
# a = crawler.crawl("a", url)
# crawler.extractLinks()
# crawler.extractForms()

# print(crawler.path)

print(crawler.linkList)
for form in crawler.__formList:
    print(form)
