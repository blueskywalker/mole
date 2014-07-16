__author__ = 'jkim'


from reppy.cache import RobotsCache
import urllib2
import nltk
import re
import zlib
import socket


class Mole:
    """ fetch web page based on robots.txt """

    def __init__(self):
        self.agent = "jerry's crawler"
        self.robots = RobotsCache()

        timeout = 60
        socket.setdefaulttimeout(timeout)

    def fetch(self, uri):
        # timeout in seconds
        if self.robots.allowed(uri, self.agent):
            req = urllib2.Request(uri)
            req.add_header('User-Agent', self.agent)
            response = urllib2.urlopen(req)
            if response.code == 200:
                return response.read()

        return None

    def filter_punctuation(self,tokens):
        non_punct = re.compile('.*[A-Za-z0-9].*')
        return [ w for w in tokens if non_punct.match(w) ]

    def get_sitexml_robots(self,url):
        robot_url = '/'.join([url, 'robots.txt'])
        content = self.fetch(robot_url)
        lines = content.split('\n')
        sitemaps=[]
        for line in lines:
            line = line.lower()
            index=line.find("sitemap")
            if index < 0 :
                continue
            m=re.search('sitemap\s*:\s*(\S+)',line[index:])
            sitemaps.append(m.group(1))

        return sitemaps

    def read_sitemap_file(self,mapfile):
        content = self.fetch(mapfile)

        if content is None:
            return None

        if mapfile.endswith('.gz'):
            d = zlib.decompressobj(16+zlib.MAX_WBITS)
            content = d.decompress(content)

        print content

if __name__ == "__main__":
    crawler = Mole()
    sitemaps=crawler.get_sitexml_robots('http://www.nytimes.com')

    for sitemap in sitemaps:
        crawler.read_sitemap_file(sitemap)
