#!/usr/bin/env python3

import os
import random
import time
import logging
import uuid



def config_log():
    log = logging.getLogger('cmonitor')
    f = logging.Formatter('%(asctime)s - %(name)s:%(process)d - %(levelname)s - %(message)s')
    h = logging.StreamHandler()
    h.setLevel(logging.DEBUG)
    h.setFormatter(f)
    log.addHandler(h)
    log.setLevel(logging.DEBUG)
    return log

def mon_cpu():
    return random.choice([
        '0x283FE8',
        '#AFEFEF',
        '2398098098'
        ])

def mon_slice():
    s = random.random()
    return random.choice([
        'Created slice User Slice of root.',
        'Starting User Slice of root.',
        'Started Session {} of user root.'.format(s),
        'Starting Session {} of user root.'.format(s),
        'Removed slice User Slice of root.' 
        ])

def monitor(log):
    while True:
        time.sleep(random.random())
        log.info('process {}'.format(uuid.uuid4()))
        log.debug(mon_slice())
        time.sleep(random.random() / 2)

if __name__ == "__main__":
    log = config_log()
    sessionid = uuid.uuid4()
    log.info('cmonitor starting {}'.format(sessionid))
    try:
        monitor(log)
    except KeyboardInterrupt as e:
        log.info('KeyboardInterrupt {}'.format(e))
        