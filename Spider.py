import re
import time
import urllib
import random
import threading

class Spider(threading.Thread):
    
    def __init__(self, pool, history, **kwargs):
        threading.Thread.__init__(self)
        
        self.pool = pool
        self.history = history

        self.ignoreextensions = (
            '.css',
            '.png',
            '.jpg',
            '.jpeg',
            '.gif'
        )

        self.args = kwargs

        self.quit = False
        
    def run(self):
        # Set the current url in the pool to assigned, but no DB (thanks Mike!)
        # Oh wait, I can't, no DB exists
        global running
        running += 1
        # Pick a url
        self.pool.sort()
        index = random.randint(0, len(self.pool)-1)
        self.url = self.pool.pop(index)

        # urllib that source straight from a url
        print "Spidering %s" % self.url

        try:
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
                if url.startswith('http') and not url.endswith(self.ignoreextensions) and url not in pool:
                    self.pool.append(url)
    
            self.history.append(self.url)

            running -= 1
        
        except:
            print 'ERROR: %s' % self.url





if __name__ == '__main__':


#    global pool
#    global history
    start = time.time()

    pool = ['http://amd.com']
    history = []

    regex = re.compile('href="([^\"]+)"')
    
    global running
    running = 0

    while True:
        try:
            if len(pool) > 0 and running <5:
                Spider(pool, history, filter=regex).start()

                print "%d/%d | %d/%d | %.02f rps | %.02f lps" % (running,5,len(history),len(pool), len(history)/(time.time()-start), len(pool)/(time.time()-start))
            time.sleep(.4)
        except:
            print "Running: %d" % running
            print "%d/%d URLs traversed" % (len(history), len(pool))
            raise
