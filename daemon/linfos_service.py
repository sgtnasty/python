
import sys, time
from daemon import Daemon
import logging

class LinfosDaemon(Daemon):

    def __init__(self, args, log, linfos):
        self.args = args
        self.log = log
        self.linfos = linfos
        super(LinfosDaemon, self).__init__()
        
    def run(self):
        while True:
            self.log.debug('LINFOS Service pulse')
            time.sleep(1)