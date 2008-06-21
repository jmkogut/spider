import re
import urllib
import threading

class Spider(threading.Thread):
    
    def __init__(self, url, **kwargs):
        threading.Thread.__init__(self)
        
        self.url = url
        self.args = kwargs
        
    def run(self):
        # Set the current url in the pool to assigned, but no DB (thanks Mike!)
        # Oh wait, I can't, no DB exists

        # urllib that source straight from a url
        source = urllib.urlopen(self.url).read()

        # From said source, capture all url-like strings
        urls = self.args["filter"].findall(source)
        urls.sort()

        # Remove duplicate urls from list
        for url in urls:
            while urls.count(url) > 1:
                urls.remove(url)
        
        # Remove non-absolute urls (because.. I only want external links for right now)
        for url in urls:
            if url.startswith('/'):
                urls.remove(url)
        
        print urls


if __name__ == '__main__':

    pool = []
    history = []

    regex = re.compile('href="([^\"]+)"')

    s = Spider('http://digg.com/', pool=pool, history=history, filter=regex)
    s.start()
