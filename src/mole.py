__author__ = 'jkim'


from reppy.cache import RobotsCache
import urllib2,cookielib
import nltk
import re
import zlib
import socket
from lxml import objectify
from datetime import date, timedelta
from pprint import pprint as pp
from workerPool import WorkerPool
import sys



class Mole:
    """ fetch web page based on robots.txt """

    def __init__(self):
        self.agent = "jerry's crawler"
        self.robots = RobotsCache()
        self.pool = None
        self.cookieJar = cookielib.CookieJar()

        timeout = 60
        socket.setdefaulttimeout(timeout)

    def fetch(self, uri):
        # timeout in seconds
        if self.robots.allowed(uri, self.agent):
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJar))
            req = urllib2.Request(uri)
            req.add_header('User-Agent', self.agent)
            response = opener.open(req)
            if response.code == 200:
                return response.read()

        return None

    def filter_punctuation(self, tokens):
        non_punct = re.compile('.*[A-Za-z0-9].*')
        return [w for w in tokens if non_punct.match(w)]

    def get_sitexml_robots(self, url):
        robot_url = '/'.join([url, 'robots.txt'])
        content = self.fetch(robot_url)
        lines = content.split('\n')
        site = []
        for line in lines:
            line = line.lower()
            index = line.find("sitemap")
            if index < 0 :
                continue
            m = re.search('sitemap\s*:\s*(\S+)',line[index:])
            site.append(m.group(1))

        return site

    def is_within_days(self, d, days=1):
        ago = date.today() - timedelta(days)
        return ago <= d

    def read_sitemap_file(self, mapfile):
        content = self.fetch(mapfile)

        if content is None:
            return None

        if mapfile.endswith('.gz'):
            d = zlib.decompressobj(16+zlib.MAX_WBITS)
            content = d.decompress(content)

        return content

    def create_thread_pool(self, size=10):
        self.pool = WorkerPool(size)

    def page2tokens(self, content):
        return nltk.word_tokenize(nltk.clean_html(content))

if __name__ == "__main__":
    from dateutil import parser
    from datetime import datetime,date

    crawler = Mole()
    sitemaps = crawler.get_sitexml_robots('http://www.nytimes.com')

    pool = WorkerPool(30)

    for sitemap in sitemaps:
        xml = crawler.read_sitemap_file(sitemap)
        if xml is not None:
            urls = objectify.fromstring(xml)
            for url in urls.url:
                if crawler.is_within_days(parser.parse(str(url.lastmod)).date()):
                    loc = str(url.loc)
                    content=crawler.fetch(loc)
                    print crawler.page2tokens(content)
                    sys.exit(1)