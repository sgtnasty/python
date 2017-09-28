
import sys, time
from daemon import Daemon
import logging

class MyDaemon(Daemon):

    def __init__(self, args, log, my):
        self.args = args
        self.log = log
        self.my = my
        super(MyDaemon, self).__init__()
        
    def run(self):
        while True:
            self.log.debug('MY Service pulse')
            time.sleep(1)