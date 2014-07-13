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


if __name__ == "__main__":
    import sys
    crawler = Mole()
    for article_url in crawler.access2nasdaq():
        page = crawler.fetch(article_url)
        if page is not None:
            raw = nltk.clean_html(str(page))
            tokens = nltk.word_tokenize(raw)
            fdist = nltk.FreqDist(tokens)
            print fdist.N()
            print fdist.B()
            print fdist.samples()
            sys.exit(0)
