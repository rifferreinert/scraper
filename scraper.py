from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.error
from concurrent.futures import ThreadPoolExecutor


def soup_link(url, maxTry = 0):
    """uses urlopen except it keeps trying to open the page maxTrys
    times before failing. If maxTrys = 0 then it will never stop trying"""
    attempt = 1
    while True:
        try:
            page = urlopen(url)
            return BeautifulSoup(page)
        except urllib.error.HTTPError as e:
            if attempt == maxTry:
                raise e
            else:
                attempt += 1
        except ConnectionResetError as e:
            if attempt == maxTry:
                raise e
            else:
                attempt += 1
     
    
def soup_links(links, numThreads = 20, maxTry = 0):
    """takes a list of url strings and returns a map object of soups. second argument
    determines the number of strings used."""
    # executor = ThreadPoolExecutor(max_workers = numThreads)
    return map(lambda x : soup_link(x, maxTry), links)

def navigate(soup, argsList):
    """takes a list of arguments and navigates using them in order as arguments""" 
    firstLoop = True
    for args in argsList:
        name = None
        attrs = None
        text = None
        if 'name' in args:
            name = args['name']
        if 'attrs' in args:
            attrs = args['attrs']
        if 'text' in args:
            text = args['text']
        soup = soup.find(name = name, attrs = attrs, text = text)
        if not soup:
            raise Exception('Could navigate to: name = {}, attrs = {}, text = {}'.format(name, attrs, text))
    return soup
