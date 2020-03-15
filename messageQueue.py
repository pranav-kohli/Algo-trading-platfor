
#import threading
import queue

class msgQueue():
    def __init__(self, **kwargs):
        self.queue = queue.Queue()
        return super().__init__(**kwargs)

    def readData(self):
        return self.queue

    def pushData(self, data):
        self.queue.put(data)

    def purgeData(self):
        self.queue = queue.Queue()
