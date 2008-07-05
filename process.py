import time
import random
import threading
import traceback

class process:
    
    def __init__(self, worker, data=[], maxthreads=5):

        # Format (lulz)
        # worker = workset[0]
        # data = workset[1]
        self.worker = worker
        self.data = data

        self.maxthreads = maxthreads
        self.queue = []
        self.process = True
    
    def run(self):
        while self.process:
            print "%i/%i threads %i / %i" % (len(self.queue), self.maxthreads, len(self.data[1]), len(self.data[0]))
            if len(self.queue) < self.maxthreads:
                thread = self.worker(self)
                self.queue.append(thread)
                thread.start()

            time.sleep(.15)

class pWorker(threading.Thread):
    
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.parent = parent

    def remove(self):
        self.parent.queue.remove(self)

if __name__ == '__main__':
    try:
        class worker(pWorker):
            def run(self):
                time.sleep(random.random()*3)
                
                print self.parent.data.pop()
                self.parent.data.append(random.random()*8)
                self.parent.data.append(random.random()*random.random()*7)
                self.remove()
                

        data = ['http://reddit.com','http://digg.com', 'http://img.4chan.org/b/']
        p = process(worker, data)
    except KeyboardInterrupt:
        print "Hold a sec, closing threads"
    except:
        traceback.print_exc()
