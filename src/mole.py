__author__ = 'jkim'

from reppy.cache import RobotsCache
from beautifulscraper import BeautifulScraper
import urllib2

class Mole:
    ''' fetch web page based on robots.txt'''
    agent = "jerry's crawler"

    def __init__(self):
        self.robots = RobotsCache()

    def fetch(self,url):
        if self.robots.allowed(url,Mole.agent):
            header= { 'User-Agent' : Mole.agent}
            req=urllib2.Request(url=url,data=None,headers=header)
            return urllib2.urlopen(req).read()

        return None

if __name__ == "__main__":
    crawler = Mole()
    url = 'http://www.nasdaq.com'
    #html= crawler.fetch(url)
    #print html
    scraper = BeautifulScraper()
    scraper.add_header('User-Agent',Mole.agent)
    body = scraper.go(url)
    section = body.find('div',{'id':'home-editors-pick'})
    for ul in section.findAll('ul'):
        print ul.find('a')


