__author__ = 'jkim'


from reppy.cache import RobotsCache
from beautifulscraper import BeautifulScraper
import nltk
import re


class Mole:
    """ fetch web page based on robots.txt """

    agent = "jerry's crawler"

    def __init__(self):
        self.robots = RobotsCache()
        self.scraper = BeautifulScraper()

    def fetch(self, uri):
        if self.robots.allowed(uri, Mole.agent):
            self.scraper.add_header('User-Agent', Mole.agent)
            return self.scraper.go(uri)
        return None

    def access2nasdaq(self):
        url = 'http://www.nasdaq.com'
        body = self.fetch(url)
        ret = []
        if body is not None:
            section = body.find('div', {'id' : 'home-editors-pick'})

            for ul in section.findAll('ul'):
                ret.append(ul.find('a')['href'])

        return ret

    def filter_punctuation(self,tokens):
        non_punct = re.compile('.*[A-Za-z0-9].*')
        return [ w for w in tokens if non_punct.match(w) ]

    def get_sitexml_robots(self,url):
        robot_url = '/'.join([url, 'robots.txt'])
        content = self.fetch(robot_url)
        lines = str(content).split('\n')
        sitemaps=[]
        for line in lines:
            line = line.lower()
            index=line.find("sitemap")
            if index < 0 :
                continue
            m=re.search('sitemap\s*:\s*(\S+)',line[index:])
            sitemaps.append(m.group(1))

        return sitemaps

    def get_sitemap_url(self,maps):
        for url in maps:


if __name__ == "__main__":
    crawler = Mole()
    sitemaps=crawler.get_sitexml_robots('http://www.nytimes.com')
