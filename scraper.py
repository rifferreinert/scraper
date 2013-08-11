from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.error
from concurrent.futures import ThreadPoolExecutor

def urlopen_trys(url, maxTrys = 0):
    """uses urlopen except it keeps trying to open the page maxTrys
    times before failing. If maxTrys = 0 then it will never stop trying"""
     
    attempt = 1
    while True:
        try:
            return urlopen(url)
        except urllib.error.HTTPError as e:
            if attempt == maxTrys:
                raise e
            else:
                attempt += 1
      
    
def soup_links(links, numThreads = 20):
    """takes a list of url strings and returns a map object of soups. second argument
    determines the number of strings used."""
    executor = ThreadPoolExecutor(max_workers = numThreads)
    return executor.map(lambda x : soup(urlopen_trys(x)), links)

class soup(BeautifulSoup):
    def navigate(self, argsList):
        """takes a list of arguments and navigates using them in order as arguments""" 
        firstLoop = True
        newSoup = self
        for args in argsList:
            print(args)
            name = None
            attrs = None
            text = None
            if 'name' in args:
                name = args['name']
            if 'attrs' in args:
                attrs = args['attrs']
            if 'text' in args:
                text = args['text']
            newSoup = newSoup.find(name = name, attrs = attrs, text = text)
            if not newSoup:
                raise Exception('Could navigate to: name = {}, attrs = {}, text = {}'.format(name, attrs, text))
        return newSoup
