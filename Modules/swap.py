#!/usr/bin/env python3

from scorpion import Scorpion

# url = "http://dhsistemas.com.br/"
# url = "https://seguro.uern.br/integra/"
# url = "https://di.uern.br/moodle/"
# url = "http://192.168.0.105/mutillidae/index.php?page=dns-lookup.php"
# url = "http://192.168.0.105/mutillidae/index.php?page=text-file-viewer.php"
# url = "http://192.168.0.105/mutillidae/index.php?page=add-to-your-blog.php"
# url = "http://192.168.0.105/mutillidae/documentation/mutillidae-installation-on-xampp-win7.pdf"
# url = "http://192.168.0.105/mutillidae/"
url = "http://192.168.0.113/dvwa/login.php"

crawler = Scorpion(url, "admin", "password")
crawler.extractLinks("http://192.168.0.113/dvwa/index.php")
# print(crawler.extractForms())
crawler.inject()
crawler.createLog()

# crawler = Scorpion(url)
# crawler.extractLinks()
# print(crawler.extractForms("http://192.168.0.105/mutillidae/index.php?page=dns-lookup.php"))
# crawler.inject()
