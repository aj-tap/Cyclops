from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup


# Start with the initial checks: robots, sitemap, 404 error and SSL/TLS scan (if HTTPS).
# Checlist
# /robots.txt
# /sitemap.xml
# /crossdomain.xml
# /clientaccesspolicy.xml
# /.well-known/

class DefaultPages:
    def __init__(self, domain):
        self.domain = str(domain)

    def queryResource(self, url):
        try:
            content = urlopen(url)
        except HTTPError as e:
            print(e)
        except URLError as e:
            print("Resource request not found")
        return content

    def getRobots(self):
        robot_page = urlopen(self.domain + "robots.txt")
        bs = BeautifulSoup(robot_page, 'html.parser')
        content = bs.get_text()
        content = bytes(content, 'UTF-8')
        return content.decode('UTF-8')

    def getSitemap(self):
        links = []
        sitemap = urlopen(self.domain + "wp-sitemap.xml")
        bs = BeautifulSoup(sitemap, "xml")
        #content = bs.find('div', {'id':'mw-content-text'}).get_text()
        for link in bs.find_all('a'):
            if 'href' in link.attrs:
                print(link['href'])
                links.append(link['href'])
        return links

    def execute(self):
        print(self.getRobots())
        #print(self.getSitemap())



#html = urlopen('http://en.wikipedia.org/wiki/Python_(programming_language)')
#bs = BeautifulSoup(html, 'html.parser')
#content = bs.get_text()
#content = bytes(content, 'UTF-8')
#content = content.decode('UTF-8')
#print(content)

