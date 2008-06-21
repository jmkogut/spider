import re
import time
import urllib
import threading

class Spider(threading.Thread):
    
    def __init__(self, pool, history, **kwargs):
        threading.Thread.__init__(self)
        
        self.pool = pool
        self.history = history

        self.args = kwargs
        
    def run(self):
        while True:
            # Set the current url in the pool to assigned, but no DB (thanks Mike!)
            # Oh wait, I can't, no DB exists
    
            # urllib that source straight from a url
            self.url = self.pool.pop()
            print "Spidering %s" % self.url
            source = urllib.urlopen(self.url).read()
    
            # From said source, capture all url-like strings
            urls = self.args["filter"].findall(source)
            urls.sort()
    
            # Remove duplicate urls from list
            for url in urls:
                while urls.count(url) != 1:
                    urls.remove(url)
            
            # Add absolute URLs to the pool
            for url in urls:
                if url.startswith('http') and url not in pool:
                    self.pool.append(url)
    
            self.history.append(self.url)
    
            time.sleep(.2)




if __name__ == '__main__':


#    global pool
#    global history

    pool = ['http://digg.com']
    history = []

    regex = re.compile('href="([^\"]+)"')

    s = Spider(pool, history, filter=regex)
    s.start()
