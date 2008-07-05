import process

import re
import time
import urllib

class worker(process.pWorker):
    def run(self):
        if len(self.parent.data[0]) > 0:
            url = self.parent.data[0].pop(0)
            self.parent.data[1].append(url)

            print ':get %s'%url
            s = urllib.urlopen(url).read()
        
            urls = self.parent.filter.findall(s)
            for url in urls:
                if url not in self.parent.data[0] and url not in self.parent.data[1]:
                    if url.startswith('http'):
                        self.parent.data[0].append(url)
        else:
            time.sleep(1)

        self.remove()

if __name__ == '__main__':
    data = [['http://bored.com'],[]]
    p = process.process(worker, data, 10)
    p.filter = re.compile('href="([^\"]+)"')
    p.run()
